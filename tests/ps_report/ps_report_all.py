from glob import glob
import re

import sys
from setup_utils import parse_command_line, configure_python_paths
from os.path import join

# -------------------------------processing command line
if len(sys.argv)>2:

    args = parse_command_line()


else: # emulate command line
    # command_line_emulation_argument_list = ['--subject','R1124J_1',
    #                                         '--experiment','PS3',
    #                                         '--workspace-dir','/scratch/busygin/PS3_joint',
    #                                         '--mount-point','',
    #                                         '--python-path','/home1/busygin/ram_utils_new_ptsa',
    #                                         '--python-path','/home1/busygin/python/ptsa_latest',
    #                                         ]

    command_line_emulation_argument_list = ['--subject','R1149N',
                                         '--experiment','PS2',
                                         '--workspace-dir','/Users/m/scratch/PS2_ms_check',
                                         # '--mount-point','/Volumes/rhino_root/',
                                         '--mount-point','//Users/m/',
                                         '--python-path','/Users/m/RAM_UTILS_GIT',
                                         '--python-path','/Users/m/PTSA_NEW_GIT',
                                         '--exit-on-no-change'
                                            ]

    args = parse_command_line(command_line_emulation_argument_list)

configure_python_paths(args.python_path)

# ------------------------------- end of processing command line

import numpy as np
from RamPipeline import RamPipeline
from ReportUtils.DependencyChangeTrackerLegacy import DependencyChangeTrackerLegacy
from ReportUtils import MissingExperimentError, MissingDataError


from FREventPreparation import FREventPreparation
from ControlEventPreparation import ControlEventPreparation
from PSEventPreparation import PSEventPreparation

from ComputeFRPowers import ComputeFRPowers
from ComputeControlPowers import ComputeControlPowers
from ComputePSPowers import ComputePSPowers

from TalPreparation import TalPreparation

from ComputeClassifier import ComputeClassifier

from ComputeControlTable import ComputeControlTable
from ComputePSTable import ComputePSTable

from ComposeSessionSummary import ComposeSessionSummary

from GenerateReportTasks import *


# turn it into command line options

class Params(object):
    def __init__(self):
        self.width = 5

        self.fr1_start_time = 0.0
        self.fr1_end_time = 1.366
        self.fr1_buf = 1.365

        self.control_start_time = -1.1
        self.control_end_time = -0.1
        self.control_buf = 1.0

        self.ps_start_time = -1.0
        self.ps_end_time = 0.0
        self.ps_buf = 1.0
        self.ps_offset = 0.1

        self.filt_order = 4

        self.freqs = np.logspace(np.log10(3), np.log10(180), 8)

        self.log_powers = True

        self.penalty_type = 'l2'
        self.C = 7.2e-4

        self.n_perm = 200

        self.include_fr1 = True
        self.include_catfr1 = True


params = Params()

class ReportPipeline(RamPipeline):
    def __init__(self, subject, experiment, workspace_dir, mount_point=None, exit_on_no_change=False):
        RamPipeline.__init__(self)
        self.exit_on_no_change = exit_on_no_change
        self.subject = subject
        self.experiment = experiment
        self.mount_point = mount_point
        self.set_workspace_dir(workspace_dir)
        dependency_tracker = DependencyChangeTrackerLegacy(subject=subject, workspace_dir=workspace_dir, mount_point=mount_point)

        self.set_dependency_tracker(dependency_tracker=dependency_tracker)

# class ReportPipeline(RamPipeline):
#     def __init__(self, subject, experiment, workspace_dir, mount_point=None):
#         RamPipeline.__init__(self)
#         self.subject = subject
#         self.experiment = experiment
#         self.mount_point = mount_point
#         self.set_workspace_dir(workspace_dir)


task = 'RAM_PS'


def find_subjects_by_task(task):
    # ev_files = glob('/data/events/%s/R*_events.mat' % task)
    ev_files = glob(args.mount_point+'/data/events/%s/R*_events.mat' % task)
    return [re.search(r'R\d\d\d\d[A-Z](_\d+)?', f).group() for f in ev_files]


subjects = find_subjects_by_task(task)
#subjects.append('TJ086')
subjects.sort()

subject_fail_list = []
subject_missing_experiment_list = []
subject_missing_data_list = []

for subject in subjects:
    print subject
    # sets up processing pipeline
    # report_pipeline = ReportPipeline(subject=subject, experiment=args.experiment,
    #                                    workspace_dir=join(args.workspace_dir,subject), mount_point=args.mount_point)

    report_pipeline = ReportPipeline(subject=subject,
                                     experiment=args.experiment,
                                     workspace_dir=join(args.workspace_dir,subject),
                                     mount_point=args.mount_point,
                                     # exit_on_no_change=args.exit_on_no_change
                                     )


    report_pipeline.add_task(FREventPreparation(params=params, mark_as_completed=False))

    report_pipeline.add_task(ControlEventPreparation(params=params, mark_as_completed=False))

    report_pipeline.add_task(PSEventPreparation(mark_as_completed=False))

    report_pipeline.add_task(TalPreparation(mark_as_completed=False))

    report_pipeline.add_task(ComputeFRPowers(params=params, mark_as_completed=True))

    report_pipeline.add_task(ComputeClassifier(params=params, mark_as_completed=True))

    report_pipeline.add_task(ComputeControlPowers(params=params, mark_as_completed=True))

    report_pipeline.add_task(ComputePSPowers(params=params, mark_as_completed=True))

    report_pipeline.add_task(ComputeControlTable(params=params, mark_as_completed=True))

    report_pipeline.add_task(ComputePSTable(params=params, mark_as_completed=True))

    report_pipeline.add_task(ComposeSessionSummary(params=params, mark_as_completed=False))

    report_pipeline.add_task(GeneratePlots(mark_as_completed=False))

    report_pipeline.add_task(GenerateTex(mark_as_completed=False))

    report_pipeline.add_task(GenerateReportPDF(mark_as_completed=False))

    # starts processing pipeline
    try:
        report_pipeline.execute_pipeline()
    except KeyboardInterrupt:
        print 'GOT KEYBOARD INTERUPT. EXITING'
        sys.exit()
    except MissingExperimentError:
        subject_missing_experiment_list.append(subject)
    except MissingDataError:
        subject_missing_data_list.append(subject)

    # except:
    #     subject_fail_list.append(subject)
    #     pass

print 'all subjects = ', subjects
print 'subject_fail_list=',subject_fail_list
print 'subject_missing_experiment_list=',subject_missing_experiment_list
print 'subject_missing_data_list=', subject_missing_data_list