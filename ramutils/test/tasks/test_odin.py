from __future__ import print_function

from collections import namedtuple
import functools
import json
import os
import os.path as osp
from unittest.mock import Mock, patch
from zipfile import ZipFile

from pkg_resources import resource_string, resource_filename

import pytest

from classiflib import ClassifierContainer

from ramutils.parameters import StimParameters, FilePaths, FRParameters
from ramutils.tasks.odin import (
    generate_ramulator_config, generate_electrode_config
)
from ramutils.montage import generate_pairs_from_electrode_config
import ramutils.test.test_data
from ramutils.utils import touch, mkdir_p


datafile = functools.partial(resource_filename, 'ramutils.test.test_data')


def jsondata(s):
    return json.loads(resource_string('ramutils.test.test_data', s))


def test_generate_electrode_config(tmpdir):
    # Make rhino-like directory structure
    subject = 'R1347D'
    docs_dir = str(
        tmpdir.join('data')
              .join('eeg')
              .join(subject)
              .join('docs')
    )
    dest = 'scratch'

    mkdir_p(docs_dir)
    mkdir_p(str(tmpdir.join(dest)))

    with open(osp.join(docs_dir, 'jacksheet.txt'), 'wb') as f:
        f.write(resource_string('ramutils.test.test_data',
                                '{}_jacksheet.txt'.format(subject)))

    with open(osp.join(docs_dir, 'area.txt'), 'wb') as f:
        f.write(resource_string('ramutils.test.test_data',
                                '{}_area.txt'.format(subject)))

    paths = FilePaths(root=str(tmpdir), dest=dest)
    anodes = None
    cathodes = None

    path = generate_electrode_config(
        subject, paths, anodes, cathodes)
    assert isinstance(path, FilePaths)


@pytest.mark.parametrize('experiment', ['AmplitudeDetermination', 'FR6'])
def test_generate_ramulator_config(experiment, output_dest):
    subject = 'R1354E'

    root = osp.join(osp.dirname(ramutils.test.test_data.__file__))
    container = Mock(ClassifierContainer)

    # Since we're putting configs in a timestamped directory, we need to find it
    # before we can save the mocked classifier
    def save_classifier():
        output_dir = osp.join(output_dest, 'output')
        subdirs = [
            osp.join(output_dir, d)
            for d in os.listdir(output_dir)
            if osp.isdir(osp.join(output_dir, d))
        ]
        timestamped_dir = max(subdirs, key=osp.getmtime)
        classifier_path = osp.join(output_dir, timestamped_dir, subject,
                                   experiment, 'config_files',
                                   '{}-classifier.zip'.format(subject))
        touch(classifier_path)

    Pairs = namedtuple('Pairs', 'label,anode,cathode')
    pairs = [Pairs('1Ld1-1Ld2', 1, 2), Pairs('1Ld3-1Ld4', 3, 4)]

    stim_params = [
        StimParameters(
            anode_label=pair.label.split('-')[0],
            cathode_label=pair.label.split('-')[1],
            anode=pair.anode,
            cathode=pair.cathode
        )
        for pair in pairs
    ]

    ec_conf_prefix = 'R1354E_26OCT2017L0M0STIM'
    paths = FilePaths(
        root=root,
        electrode_config_file='/input/configs/R1354E_26OCT2017L0M0STIM' +
                              '.csv',

        # Since we're not actually reading the pairs files in this test, we
        # don't have to worry about the fact that the subjects aren't the same.
        # All we are really doing in this test is verifying that stuff is saved.
        pairs='/input/configs/R1328E_pairs.json',
    )
    paths.dest = os.path.join(output_dest, 'output')

    getpath = functools.partial(resource_filename, 'ramutils.test.test_data')
    with open(getpath('/input/configs/R1328E_excluded_pairs.json'), 'r') as f:
        excluded_pairs = json.load(f)

    if "FR" in experiment:
        exp_params = FRParameters()
    elif experiment == "AmplitudeDetermination":
        exp_params = None
    else:
        raise RuntimeError("invalid experiment")

    with patch.object(container, 'save',
                      side_effect=lambda *_, **__: save_classifier()):
        path = generate_ramulator_config(subject, experiment, container,
                                         stim_params, paths,
                                         excluded_pairs=excluded_pairs,
                                         exp_params=exp_params)
        container.save.assert_called_once()

    with ZipFile(path) as zf:
        members = zf.namelist()

    assert 'experiment_config.json' in members
    if experiment != 'AmplitudeDetermination':
        assert 'exp_params.h5' in members
        assert 'config_files/{}-classifier.zip'.format(subject) in members
    assert 'config_files/pairs.json' in members
    assert 'config_files/excluded_pairs.json' in members
    assert 'config_files/' + ec_conf_prefix + '.csv' in members
    assert 'config_files/' + ec_conf_prefix + '.bin' in members
