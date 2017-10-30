"""command line example::

    python fr3_util_system_3.py --workspace-dir=/scratch/busygin/FR3_biomarkers --subject=R1145J_1 --n-channels=128 --anode=RD2 --anode-num=34 --cathode=RD3 --cathode-num=35 --pulse-frequency=200 --pulse-duration=500 --target-amplitude=1000

"""

from __future__ import print_function

import numpy as np

from ramutils.pipeline import RamPipeline
from tests.fr5_biomarker.FREventPreparation import FREventPreparation
from tests.fr5_biomarker.ComputeFRPowers import ComputeFRPowers
from tests.fr5_biomarker.MontagePreparation import MontagePreparation
from tests.fr5_biomarker.ComputeClassifier import (
    ComputeClassifier, ComputeFullClassifier, ComputeEncodingClassifier
)
from tests.fr5_biomarker.system3.ExperimentConfigGeneratorClosedLoop5 import ExperimentConfigGeneratorClosedLoop5
from system_3_utils.ram_tasks.CheckElectrodeConfigurationClosedLoop3 import CheckElectrodeConfigurationClosedLoop3
from system_3_utils.ram_tasks.CMLParserClosedLoop3 import CMLParserCloseLoop3


print("ATTN: Wavelet params and interval length are hardcoded!! To change them, recompile")
print("Windows binaries from https://github.com/busygin/morlet_for_sys2_biomarker")
print("See https://github.com/busygin/morlet_for_sys2_biomarker/blob/master/README for detail.")

cml_parser = CMLParserCloseLoop3()

# These arguments are only used if command-line arguments are not given
cml_parser.arg('--workspace-dir', '/Users/depalati/mnt/rhino/scratch/depalati/configs')
cml_parser.arg('--experiment', 'FR5')
cml_parser.arg('--mount-point', '/Users/depalati/mnt/rhino')
cml_parser.arg('--subject', 'R1308T')
cml_parser.arg('--electrode-config-file', '/Users/depalati/mnt/rhino/scratch/system3_configs/ODIN_configs/R1308T/R1308T_14JUN2017L0M0STIM.csv')
cml_parser.arg('--pulse-frequency', '200')
cml_parser.arg('--target-amplitude', '1.0')
cml_parser.arg('--anodes', 'LB6')
cml_parser.arg('--cathodes', 'LB7')
cml_parser.arg('--min-amplitudes', '0.1')
cml_parser.arg('--max-amplitudes', '0.5')

args = cml_parser.parse()


class StimParams(object):
    def __init__(self, **kwds):
        pass


class Params(object):
    def __init__(self):
        self.version = '3.00'

        self.include_fr1 = True
        self.include_catfr1 = True
        self.include_fr3 = False
        self.include_catfr3 = False

        self.width = 5

        self.fr1_start_time = 0.0
        self.fr1_end_time = 1.366
        self.fr1_buf = 1.365

        self.fr1_retrieval_start_time = -0.525
        self.fr1_retrieval_end_time = 0.0
        self.fr1_retrieval_buf = 0.524

        self.encoding_samples_weight = 2.5

        self.filt_order = 4

        self.freqs = np.logspace(np.log10(6), np.log10(180), 8)

        self.log_powers = True

        self.penalty_type = 'l2'
        self.C = 7.2e-4

        self.n_perm = 200

        self.stim_params = StimParams()


class ReportPipeline(RamPipeline):
    def __init__(self, subject, workspace_dir, mount_point=None, args=None):
        RamPipeline.__init__(self)
        self.subject = subject
        self.mount_point = mount_point
        self.set_workspace_dir(workspace_dir)
        self.args = args


if __name__ == "__main__":
    params = Params()
    mark_as_completed = True

    pipeline = ReportPipeline(subject=args.subject,
                              workspace_dir=args.workspace_dir,
                              mount_point=args.mount_point,
                              args=args)

    pipeline.add_task(FREventPreparation(mark_as_completed=mark_as_completed))
    pipeline.add_task(MontagePreparation(mark_as_completed=mark_as_completed, force_rerun=True))
    pipeline.add_task(CheckElectrodeConfigurationClosedLoop3(
        params=params, mark_as_completed=False, force_rerun=True))
    pipeline.add_task(ComputeFRPowers(params=params, mark_as_completed=mark_as_completed))

    if args.encoding_only:
        pipeline.add_task(ComputeEncodingClassifier(params=params, mark_as_completed=mark_as_completed, force_rerun=True))
    else:
        pipeline.add_task(ComputeClassifier(params=params, mark_as_completed=mark_as_completed, force_rerun=False))

    pipeline.add_task(ComputeFullClassifier(params=params, mark_as_completed=mark_as_completed))
    pipeline.add_task(ExperimentConfigGeneratorClosedLoop5(params=params, mark_as_completed=False))

    pipeline.execute_pipeline()
