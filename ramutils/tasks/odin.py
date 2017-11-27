"""Tasks specific to the Medtronic Odin ENS."""

from collections import OrderedDict
import functools
import json
import os.path
from tempfile import gettempdir
import shutil
import warnings

try:
    from typing import List
except ImportError:
    pass

from bptools.transform import SeriesTransformation
from classiflib import ClassifierContainer

from ramutils.constants import EXPERIMENTS
from ramutils.log import get_logger
from ramutils.tasks import task
from ramutils.utils import reindent_json

__all__ = ['generate_pairs_from_electrode_config', 'generate_ramulator_config']

CLASSIFIER_VERSION = "1.0.2"

logger = get_logger()


# FIXME: logic for generating pairs should be in bptools
@task()
def generate_pairs_from_electrode_config(subject, paths):
    """Load and verify the validity of the Odin electrode configuration file.

    :param str subject: Subject ID
    :param FilePaths paths:
    :returns: minimal pairs.json based on the electrode configuration
    :rtype: dict
    :raises RuntimeError: if the csv or bin file are not found

    """
    prefix, _ = os.path.splitext(paths.electrode_config_file)
    csv_filename = prefix + '.csv'
    bin_filename = prefix + '.bin'

    if not os.path.exists(csv_filename):
        raise RuntimeError("{} not found!".format(csv_filename))
    if not os.path.exists(bin_filename):
        raise RuntimeError("{} not found!".format(bin_filename))

    # Create SeriesTransformation object to determine if this is monopolar,
    # mixed-mode, or bipolar
    # FIXME: load excluded pairs
    xform = SeriesTransformation.create(csv_filename, paths.pairs)

    # Odin electrode configuration
    ec = xform.elec_conf

    # This will mimic pairs.json (but only with labels).
    pairs_dict = OrderedDict()

    # FIXME: move the following logic into bptools
    # Hardware bipolar mode
    if not xform.monopolar_possible():
        contacts = ec.contacts_as_recarray()

        for ch in ec.sense_channels:
            anode, cathode = ch.contact, ch.ref
            aname = contacts[contacts.jack_box_num == anode].contact_name[0]
            cname = contacts[contacts.jack_box_num == cathode].contact_name[0]
            name = '{}-{}'.format(aname, cname)
            pairs_dict[name] = {
                'channel_1': anode,
                'channel_2': cathode
            }

        # Note this is different from neurorad pipeline pairs.json because
        # the electrode configuration trumps it
        pairs_from_ec = {subject: {'pairs': pairs_dict}}

        return pairs_from_ec


def _make_experiment_specific_data_section(experiment, stim_params,
                                           classifier_file,
                                           classifier_version=CLASSIFIER_VERSION):
    """Return a dict containing the config section ``experiment_specific_data``.

    Parameters
    ----------
    experiment : str
    stim_params : dict
    classifier_file : str
    classifier_version : str

    Returns
    -------
    dict representation of the ``experiment_specific_data`` section.

    """
    def make_stim_channel_section(params, key):
        stub = {
            "stim_duration": 500,
            "stim_frequency": 200
        }

        if 'PS4' in experiment:
            stub.update({
                'min_stim_amplitude': params[key]['min_stim_amplitude'],
                'max_stim_amplitude': params[key]['max_stim_amplitude']
            })
        else:
            stub.update({
                'stim_amplitude': params[key]['stim_amplitude']
            })

        return stub

    esd = {
        "allow_classifier_generalization": True,
        "classifier_file": classifier_file,
        "classifier_version": classifier_version,
        "random_stim_prob": False,
        "save_debug_output": True,
        "stim_channels": {
            label: make_stim_channel_section(stim_params, label)
            for label in stim_params
        }
    }

    return esd


def _make_experiment_specs_section(experiment):
    """Generate the ``experiment_specs`` config section.

    Parameters
    ----------
    experiment : str

    Returns
    -------
    ``experiment_specs`` dict

    """
    # FIXME: values below shouldn't be hardcoded
    specs = {
        "version": "3.0.0",
        "experiment_type": experiment,
        "biomarker_sample_start_time_offset": 0,
        "biomarker_sample_time_length": 1366,
        "buffer_time": 1365,
        "stim_duration": 500,
        "freq_min": 6,
        "freq_max": 180,
        "num_freqs": 8,
        "num_items": 300,
    }

    # FIXME: values below shouldn't be hardcoded
    if 'PS4' in experiment:
        specs.update({
            "retrieval_biomarker_sample_start_time_offset": 0,
            "retrieval_biomarker_sample_time_length": 525,
            "retrieval_buffer_time": 524,
            "post_stim_biomarker_sample_time_length": 500,
            "post_stim_buffer_time": 499,
            "post_stim_wait_time": 100,
        })

    return specs


def _make_ramulator_config_json(subject, experiment, electrode_config_file,
                                stim_params, classifier_file=None,
                                classifier_version=None):
    """Create the Ramulator ``experiment_config.json`` file.

    Parameters
    ----------
    subject : str
    experiment : str
    electrode_config_file : str
    stim_params : dict
    classifier_file : str
    classifier_version : str

    Returns
    -------
    str

    """
    config = {
        'subject': subject,
        'experiment': {
            'type': experiment,
            'experiment_specific_data':
                _make_experiment_specific_data_section(experiment,
                                                       stim_params,
                                                       classifier_file,
                                                       classifier_version),
            'experiment_specs': _make_experiment_specs_section(experiment),
        },

        # FIXME: are these the right defaults?
        'artifact_detection': {
            "allow_artifact_detection": True,
            "artifact_detection_number_of_stims_per_channel": 15,
            "artifact_detection_sample_time_length": 500,
            "artifact_detection_inter_stim_interval": 2000,
            "allow_artifact_detection_during_session": False
        },

        "biomarker_threshold": 0.5,
        "electrode_config_file": "config_files/{}".format(electrode_config_file),
        "montage_file": "config_files/pairs.json",
        "excluded_montage_file": "config_files/excluded_pairs.json",
        "global_settings": {
            "data_dir": "SET_AUTOMATICALLY_AT_A_RUNTIME",
            "experiment_config_filename": "SET_AUTOMATICALLY_AT_A_RUNTIME",
            "extended_blanking": True,  # FIXME: make a parameter
            "plot_fps": 5,
            "plot_window_length": 20000,
            "plot_update_style": "Sweeping",
            "max_session_length": 120,
            "sampling_rate": 1000,
            "odin_lib_debug_level": 0,
            "connect_to_task_laptop": True if experiment != 'AmplitudeDetermination' else False
        }
    }

    return json.dumps(config, indent=2, sort_keys=True)


@task(cache=False)
def generate_ramulator_config(subject, experiment, container, stim_params,
                              paths, pairs=None, excluded_pairs=None,
                              params=None):
    """Create configuration files for Ramulator.

    Note that the current template format will not work for FR5 experiments
    since the config format is not the same.

    In hardware bipolar mode, the neurorad pipeline generates a ``pairs.json``
    file that differs from the electrode configured pairs. It is up to the user
    of the pipeline to ensure that the path to the correct ``pairs.json`` is
    supplied (although Ramulator does not use it in this case).

    The destination path is assumed to be relative to the root path. All other
    paths are assumed to be absolute.

    :param str subject:
    :param str experiment:
    :param ClassifierContainer container: serialized classifier
    :param List[StimParameters] stim_params: list of stimulation parameters
    :param FilePaths paths:
    :param dict excluded_pairs: Pairs excluded from the classifier (pairs that
        contain a stim contact and possibly some others)
    :param ExperimentParameters params: All parameters used in training the
        classifier. This is partially redundant with some data stored in the
        ``container`` object.
    :returns: path to generated configuration zip file
    :rtype: str

    """
    subject = subject.split('_')[0]

    stim_dict = {
        stim_param.label: {
            "min_stim_amplitude": stim_param.min_amplitude,
            "max_stim_amplitude": stim_param.max_amplitude,
            "stim_frequency": stim_param.frequency,
            "stim_duration": stim_param.duration,
            "stim_amplitude": stim_param.target_amplitude,
        }
        for stim_param in stim_params
    }

    dest = paths.dest
    config_dir_root = os.path.join(dest, subject, experiment)
    config_files_dir = os.path.join(config_dir_root, 'config_files')
    try:
        os.makedirs(config_files_dir)
    except OSError as e:
        if e.errno != 17:  # File exists
            raise

    classifier_path = os.path.join(config_files_dir, '{}-classifier.zip'.format(subject))
    ec_prefix, _ = os.path.splitext(paths.electrode_config_file)

    experiment_config_content = _make_ramulator_config_json(
        subject, experiment, os.path.basename(ec_prefix + '.bin'), stim_dict,
        os.path.basename(classifier_path), CLASSIFIER_VERSION
    )

    with open(os.path.join(config_dir_root, 'experiment_config.json'), 'w') as f:
        tmp_path = os.path.join(gettempdir(), "experiment_config.json")
        with open(tmp_path, 'w') as tmpfile:
            tmpfile.write(experiment_config_content)
        f.write(reindent_json(tmp_path))

    if experiment != 'AmplitudeDetermination':
        container.save(classifier_path, overwrite=True)

    # Save some typing below...
    conffile = functools.partial(os.path.join, config_files_dir)

    # Write pairs.json and excluded_pairs.json to the config directory. We can
    # give pairs.json as a parameter (generally when read from the electrode
    # config file) or as a path (when using the neurorad pipeline's pairs.json).
    if pairs is not None:
        with open(conffile('pairs.json'), 'w') as f:
            json.dump(pairs, f)
    else:
        shutil.copy(paths.pairs, conffile('pairs.json'))
    if excluded_pairs is not None:
        # Make format of excluded pairs more standard
        excluded_pairs = {subject: {'pairs': excluded_pairs}}
        with open(conffile('excluded_pairs.json'), 'w') as f:
            json.dump(excluded_pairs, f)

    # Copy electrode config files
    csv = paths.electrode_config_file
    bin = csv.replace('.csv', '.bin')
    shutil.copy(csv, conffile(os.path.basename(csv)))
    shutil.copy(bin, conffile(os.path.basename(bin)))

    # Serialize experiment parameters
    if params is not None:
        params.to_hdf(os.path.join(config_dir_root, 'exp_params.h5'))
    else:
        if experiment not in ['AmplitudeDetermination'] + EXPERIMENTS['record_only']:
            warnings.warn("No ExperimentParameters object passed; "
                          "classifier may not be 100% reproducible", UserWarning)

    zip_prefix = os.path.join(dest, '{}_{}'.format(subject, experiment))
    zip_path = zip_prefix + '.zip'
    shutil.make_archive(zip_prefix, 'zip', root_dir=config_dir_root)
    logger.info("Created experiment_config zip file: %s", zip_path)
    return zip_path
