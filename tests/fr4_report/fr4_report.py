import sys
from os.path import *


from ReportUtils import CMLParser,ReportPipeline




cml_parser = CMLParser(arg_count_threshold=1)
cml_parser.arg('--subject','R1076D')
cml_parser.arg('--task','RAM_FR4')
cml_parser.arg('--workspace-dir','/Users/busygin/scratch/FR4_reports')
cml_parser.arg('--mount-point','/Volumes/RHINO')
cml_parser.arg('--recompute-on-no-status')
cml_parser.arg('--python-path','/Users/busygin/ram_utils_new_ptsa')
cml_parser.arg('--python-path','/Users/busygin/ptsa_latest')
cml_parser.arg('--python-path','/Users/busygin/cpp/morlet_install')


args = cml_parser.parse()

#
# from setup_utils import parse_command_line, configure_python_paths
#
# # -------------------------------processing command line
# if len(sys.argv)>2:
#
#     args = parse_command_line()
#
#
# else: # emulate command line
#     # command_line_emulation_argument_list = ['--subject','R1124J_1',
#     #                                         '--task','RAM_FR3',
#     #                                         '--workspace-dir','/scratch/busygin/FR3_reports',
#     #                                         '--mount-point','',
#     #                                         '--python-path','/home1/busygin/ram_utils',
#     #                                         '--python-path','/home1/busygin/python/ptsa/build/lib.linux-x86_64-2.7'
#     #                                         ]
#
#     # command_line_emulation_argument_list = ['--subject','R1076D',
#     #                                         '--task','RAM_FR4',
#     #                                         '--workspace-dir','/scratch/busygin/FR4_reports',
#     #                                         '--mount-point','',
#     #                                         '--python-path','/home1/busygin/ram_utils',
#     #                                         '--python-path','/home1/busygin/python/ptsa_latest'
#     #                                         ]
#
#     command_line_emulation_argument_list = ['--subject', 'R1076D',
#                                             '--task', 'RAM_FR4',
#                                             '--workspace-dir', '/scratch/mswat/FR4_reports',
#                                             '--mount-point', '',
#                                             # '--python-path', '/home1/busygin/ram_utils',
#                                             # '--python-path', '/home1/busygin/python/ptsa_latest'
#                                             ]
#
#
#     # command_line_emulation_argument_list = ['--subject', 'R1076D',
#     #                                         '--task', 'RAM_FR4',
#     #                                         '--workspace-dir', 'scratch/mswat/FR4_reports',
#     #                                         '--mount-point', '/Volumes/rhino_root',
#     #                                         '--python-path', '/Users/m/RAM_UTILS_GIT',
#     #                                         '--python-path', '/Users/m/PTSA_NEW_GIT'
#     #                                         ]
#
#     args = parse_command_line(command_line_emulation_argument_list)
#
# configure_python_paths(args.python_path)
#
# # ------------------------------- end of processing command line

import numpy as np
from RamPipeline import RamPipeline
from RamPipeline import RamTask

from FREventPreparation import FREventPreparation

from EventPreparation import EventPreparation

from MathEventPreparation import MathEventPreparation

from ComputeFRPowers import ComputeFRPowers

from ComputeClassifier import ComputeClassifier

from ComputeFR4Powers import ComputeFR4Powers

from TalPreparation import TalPreparation

from ComputeFR4Table import ComputeFR4Table

from ComposeSessionSummary import ComposeSessionSummary

from GenerateReportTasks import *


# turn it into command line options

class Params(object):
    def __init__(self):
        self.fr4_exclude_first_3_lists = True

        self.width = 5

        self.fr1_start_time = 0.0
        self.fr1_end_time = 1.366
        self.fr1_buf = 1.365

        self.filt_order = 4

        self.freqs = np.logspace(np.log10(3), np.log10(180), 8)

        self.log_powers = True

        self.ttest_frange = (70.0, 200.0)

        self.penalty_type = 'l2'
        self.C = 7.2e-4

        self.n_perm = 200

        self.include_fr1 = True
        self.include_catfr1 = True


params = Params()

#
# class ReportPipeline(RamPipeline):
#     def __init__(self, subject, task, workspace_dir, mount_point=None):
#         RamPipeline.__init__(self)
#         self.subject = subject
#         self.task = self.experiment = task
#         self.mount_point = mount_point
#         self.set_workspace_dir(workspace_dir)

# sets up processing pipeline
report_pipeline = ReportPipeline(subject=args.subject, task=args.task,experiment=args.task,
                                 workspace_dir=join(args.workspace_dir,args.task+'_'+args.subject), mount_point=args.mount_point, exit_on_no_change=args.exit_on_no_change,
                                 recompute_on_no_status=args.recompute_on_no_status)




# sets up processing pipeline
# report_pipeline = ReportPipeline(subject=args.subject, task=args.task,
#                                        workspace_dir=join(args.workspace_dir,args.task+'_'+args.subject), mount_point=args.mount_point)
#

report_pipeline.add_task(FREventPreparation(params=params, mark_as_completed=False))

report_pipeline.add_task(EventPreparation(mark_as_completed=False))

report_pipeline.add_task(MathEventPreparation(mark_as_completed=False))

report_pipeline.add_task(TalPreparation(mark_as_completed=False))

report_pipeline.add_task(ComputeFRPowers(params=params, mark_as_completed=True))

report_pipeline.add_task(ComputeClassifier(params=params, mark_as_completed=True))

report_pipeline.add_task(ComputeFR4Powers(params=params, mark_as_completed=True))

report_pipeline.add_task(ComputeFR4Table(params=params, mark_as_completed=True))

report_pipeline.add_task(ComposeSessionSummary(params=params, mark_as_completed=False))
#
report_pipeline.add_task(GeneratePlots(mark_as_completed=False))
#
report_pipeline.add_task(GenerateTex(mark_as_completed=False))
#
report_pipeline.add_task(GenerateReportPDF(mark_as_completed=False))

# starts processing pipeline
report_pipeline.execute_pipeline()
