import sys
import os

from ptsa.data.readers.IndexReader import JsonIndexReader

from ReportUtils import CMLParser,ReportPipeline


cml_parser = CMLParser(arg_count_threshold=1)
cml_parser.arg('--task','FR2')
cml_parser.arg('--workspace-dir','/scratch/RAM_maint/automated_reports_json/FR1_reports')
cml_parser.arg('--mount-point','')
cml_parser.arg('--recompute-on-no-status')
cml_parser.arg('--hf_num')
cml_parser.arg('--stim')

# cml_parser.arg('--exit-on-no-change')

#cml_parser.arg('--task','FR1')
#cml_parser.arg('--workspace-dir','/scratch/RAM_maint/automated_reports/FR1_reports')
# cml_parser.arg('--mount-point','/Users/m')
#cml_parser.arg('--recompute-on-no-status')
# cml_parser.arg('--python-path','/Users/m/PTSA_NEW_GIT')
#cml_parser.arg('--exit-on-no-change')


args = cml_parser.parse()



from ReportUtils import ReportSummaryInventory, ReportSummary
from ReportUtils import ReportPipelineBase


if args.use_matlab_events:
    from FR2MatEventPreparation import FR2EventPreparation
else:
    from FR2EventPreparation import FR2EventPreparation

from ComputeFR2Powers import ComputeFR2Powers

from MontagePreparation import MontagePreparation

from ComputeFR2HFPowers import ComputeFR2HFPowers

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

        if not args.hf_num:
            self.hfs = np.logspace(np.log10(2), np.log10(200), 50)
            self.hfs = self.hfs[self.hfs>=70.0]
        else:
            self.hfs = np.logspace(np.log10(float(args.hf_min)),np.log10(float(args.hf_max)),int(args.hf_num))

        self.stim = True if args.stim.capitalize()=='True' else (False if args.stim.capitalize()=='False' else None)

        self.log_powers = True

        self.penalty_type = 'l2'
        self.C = 7.2e-4

        self.n_perm = 200


params = Params()

args.task = args.task.upper()

if 'CAT' in args.task:
    args.task='cat'+args.task.split('CAT')[1]



json_reader = JsonIndexReader(os.path.join(args.mount_point,'protocols/r1.json'))
subject_set = json_reader.aggregate_values('subjects', experiment=args.task)
subjects = []
for s in subject_set:
    montages = json_reader.aggregate_values('montage', subject=s, experiment=args.task)
    for m_ in montages:
        m = str(m_)
        subject = str(s)
        if m!='0':
            subject += '_' + m
        subjects.append(subject)
subjects.sort()

print 'task:',args.task
print 'stim:',params.stim

rsi = ReportSummaryInventory(label=args.task)


for subject in subjects:
    if args.skip_subjects is not None and subject in args.skip_subjects:
        continue
    print '--Generating', args.task, 'report for', subject

    # sets up processing pipeline
    # report_pipeline = ReportPipeline(subject=subject, task=task, experiment=task,
    #                                        workspace_dir=join(args.workspace_dir,task+'_'+subject), mount_point=args.mount_point, exit_on_no_change=args.exit_on_no_change,recompute_on_no_status=args.recompute_on_no_status)


    # report_pipeline = ReportPipeline(subject=subject, task=task, experiment=task,
    #                                  workspace_dir=join(args.workspace_dir, task + '_' + subject),
    #                                  mount_point=args.mount_point, exit_on_no_change=args.exit_on_no_change,
    #                                  recompute_on_no_status=args.recompute_on_no_status)

    report_pipeline = ReportPipeline(
                                     args=args,
                                     subject=subject,
                                     workspace_dir=join(args.workspace_dir, args.task + '_' + subject)
                                     )

    report_pipeline.add_task(FR2EventPreparation(params=params, mark_as_completed=False))

    report_pipeline.add_task(MontagePreparation(params=params, mark_as_completed=False))

    name = '' if params.stim is None else('Stim' if params.stim is True else 'NoStim')

    report_pipeline.add_task(
        ComputeFR2Powers(params=params, mark_as_completed=True, name='ComputeFR1' + name + 'Powers'))

    report_pipeline.add_task(
        ComputeFR2HFPowers(params=params, mark_as_completed=True, name='ComputeFR1HF' + name + 'Powers'))

    report_pipeline.add_task(ComputeTTest(params=params, mark_as_completed=False, name='Compute' + name + 'TTest'))

    report_pipeline.add_task(
        ComputeClassifier(params=params, mark_as_completed=True, name='Compute' + name + 'Classifier'))

    report_pipeline.add_task(ComposeSessionSummary(params=params, mark_as_completed=False))

    report_pipeline.add_task(GeneratePlots(mark_as_completed=False))

    report_pipeline.add_task(GenerateTex(mark_as_completed=False))

    report_pipeline.add_task(GenerateReportPDF(mark_as_completed=False))

    # report_pipeline.add_task(DeployReportPDF(mark_as_completed=False))

    report_pipeline.execute_pipeline()

    rsi.add_report_summary(report_summary=report_pipeline.get_report_summary())


print 'this is summary for all reports report ', rsi.compose_summary(detail_level=1)

# rsi.output_json_files(dir=args.status_output_dir)
#rsi.send_email_digest()
