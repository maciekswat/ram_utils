# command line example:
# python ps_report.py --subject=R1056M --task=FR1 --workspace-dir=~/scratch/py_9 --matlab-path=~/eeg --matlab-path=~/matlab/beh_toolbox --matlab-path=~/RAM/RAM_reporting --matlab-path=~/RAM/RAM_sys2Biomarkers --python-path=~/RAM_UTILS_GIT

# python ps_report.py --subject=R1056M --task=FR1 --workspace-dir=/data10/scratch/mswat/py_run_9 --matlab-path=~/eeg --matlab-path=~/matlab/beh_toolbox --matlab-path=~/RAM/RAM_reporting --matlab-path=~/RAM/RAM_sys2Biomarkers --python-path=~/RAM_UTILS_GIT

# python ps_report.py --subject=R1086M --task=FR1 --workspace-dir=/data10/scratch/mswat/R1086M_2 --matlab-path=~/eeg --matlab-path=~/matlab/beh_toolbox --matlab-path=~/RAM/RAM_reporting --matlab-path=~/RAM/RAM_sys2Biomarkers --matlab-path=~/RAM_UTILS_GIT/tests/ps2_report/AuxiliaryMatlab --python-path=~/RAM_UTILS_GIT
import sys

from setup_utils import parse_command_line, configure_python_paths

from ReportUtils import CMLParser, ReportPipeline

cml_parser = CMLParser(arg_count_threshold=1)
cml_parser.arg('--subject','R1147P')
cml_parser.arg('--workspace-dir','/scratch/mswat/automated_reports/FR1_CatFr1_check_1')
cml_parser.arg('--mount-point','')
cml_parser.arg('--recompute-on-no-status')
# cml_parser.arg('--exit-on-no-change')

args = cml_parser.parse()



# # -------------------------------processing command line
# if len(sys.argv)>1:
#
#     args = parse_command_line()
#
#
# else: # emulate command line
#     # command_line_emulation_argument_list = ['--subject','R1147P',
#     #                                         '--workspace-dir','/scratch/busygin/FR1_joint_reports',
#     #                                         '--mount-point','',
#     #                                         '--python-path','/home1/busygin/ram_utils_new_ptsa',
#     #                                         '--python-path','/home1/busygin/python/ptsa_latest'
#     #                                         # '--exit-on-no-change'
#     #                                         ]
#
#     command_line_emulation_argument_list = ['--subject','R1147P',
#                                             # '--task','RAM_FR1',
#                                             '--workspace-dir','/scratch/mswat/FR1_joint_reports_check',
#                                             '--mount-point','',
#                                             '--python-path','/home1/mswat/RAM_UTILS_GIT',
#                                             '--python-path','/home1/mswat/PTSA_NEW_GIT',
#                                             '--python-path','/home1/mswat/extra_libs'
#                                             # '--exit-on-no-change'
#                                             ]
#
#     args = parse_command_line(command_line_emulation_argument_list)
#
# configure_python_paths(args.python_path)

# ------------------------------- end of processing command line

from ReportUtils import ReportPipelineBase

from FR1EventPreparation import FR1EventPreparation

from MathEventPreparation import MathEventPreparation

from ComputeFR1Powers import ComputeFR1Powers

from TalPreparation import TalPreparation

from GetLocalization import GetLocalization

from ComputeFR1HFPowers import ComputeFR1HFPowers

from ComputeTTest import ComputeTTest

from ComputeClassifier import ComputeClassifier

from ComposeSessionSummary import ComposeSessionSummary

from GenerateReportTasks import *


# turn it into command line options

class Params(object):
    def __init__(self):
        self.width = 5

        self.fr1_start_time = 0.0
        self.fr1_end_time = 1.366
        self.fr1_buf = 1.365

        self.hfs_start_time = 0.0
        self.hfs_end_time = 1.6
        self.hfs_buf = 1.0

        self.filt_order = 4

        self.freqs = np.logspace(np.log10(3), np.log10(180), 8)
        self.hfs = np.logspace(np.log10(2), np.log10(200), 50)
        self.hfs = self.hfs[self.hfs>=70.0]

        self.log_powers = True

        self.penalty_type = 'l2'
        self.C = 7.2e-4

        self.n_perm = 200


params = Params()



# class ReportPipeline(ReportPipelineBase):
#     def __init__(self, subject, workspace_dir, mount_point=None, exit_on_no_change=False):
#         super(ReportPipeline,self).__init__(subject=subject, workspace_dir=workspace_dir, mount_point=mount_point, exit_on_no_change=exit_on_no_change)
#         self.task = self.experiment = 'RAM_FR1_CatFR1_joint'
#

# class ReportPipeline(ReportPipelineBase):
#     def __init__(self, subject, workspace_dir, mount_point=None, exit_on_no_change=False,recompute_on_no_status=False):
#         super(ReportPipeline,self).__init__(subject=subject, workspace_dir=workspace_dir, mount_point=mount_point, exit_on_no_change=exit_on_no_change,recompute_on_no_status=recompute_on_no_status)
#
#
#         self.task = 'RAM_FR1_CatFR1_joint'
#         self.experiment = self.task


# sets up processing pipeline
# report_pipeline = ReportPipeline(subject=args.subject,
#                                        workspace_dir=join(args.workspace_dir,args.subject), mount_point=args.mount_point, exit_on_no_change=args.exit_on_no_change)

report_pipeline = ReportPipeline(subject=args.subject,
                                 workspace_dir=join(args.workspace_dir, args.subject),
                                 task='RAM_FR1_CatFR1_joint',
                                 experiment='RAM_FR1_CatFR1_joint',
                                 mount_point=args.mount_point,
                                 exit_on_no_change=args.exit_on_no_change,
                                 recompute_on_no_status=args.recompute_on_no_status)

report_pipeline.add_task(FR1EventPreparation(mark_as_completed=False))

report_pipeline.add_task(MathEventPreparation(mark_as_completed=False))

report_pipeline.add_task(TalPreparation(mark_as_completed=False))

report_pipeline.add_task(GetLocalization(mark_as_completed=False))

report_pipeline.add_task(ComputeFR1Powers(params=params, mark_as_completed=True))

report_pipeline.add_task(ComputeFR1HFPowers(params=params, mark_as_completed=True))

report_pipeline.add_task(ComputeTTest(params=params, mark_as_completed=False))

report_pipeline.add_task(ComputeClassifier(params=params, mark_as_completed=True))

report_pipeline.add_task(ComposeSessionSummary(params=params, mark_as_completed=False))

report_pipeline.add_task(GeneratePlots(mark_as_completed=False))

report_pipeline.add_task(GenerateTex(mark_as_completed=False))

report_pipeline.add_task(GenerateReportPDF(mark_as_completed=False))

# report_pipeline.add_task(DeployReportPDF(mark_as_completed=False))


# starts processing pipeline
report_pipeline.execute_pipeline()
