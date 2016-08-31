from RamPipeline import *

from math import log
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from bisect import bisect_right
from scipy.stats import norm
import sys
from scipy.stats import describe
from ReportUtils import ReportRamTask

# def prob2perf(probs, true_labels, p):
#     idx = bisect_right(probs, p)
#     return np.sum(true_labels[0:idx]) / float(idx) if idx>0 else 0.0


def prob2perf_norm(xval_output, p):
    fi1 = fi0 = 1.0

    if p < 1e-6:
        return 0.0
    elif p < 1.0 - 1e-6:
        p_norm = log(p/(1.0-p))
        fi1 = norm.cdf(p_norm, loc=xval_output.mean1, scale=xval_output.pooled_std)
        fi0 = norm.cdf(p_norm, loc=xval_output.mean0, scale=xval_output.pooled_std)

    r = xval_output.n1*fi1 / (xval_output.n1*fi1 + xval_output.n0*fi0)
    return r


def bipolar_label_to_loc_tag(bp, loc_tags):
    if bp=='' or bp=='[]':
        return None
    label = bp[0]+'-'+bp[1]
    if label in loc_tags:
        lt = loc_tags[label]
        return lt if lt!='' and lt!='[]' else None
    label = bp[1]+'-'+bp[0]
    if label in loc_tags:
        lt = loc_tags[label]
        return lt if lt!='' and lt!='[]' else None
    else:
        return None


class ComputePSTable(ReportRamTask):
    def __init__(self, params, mark_as_completed=True):
        super(ComputePSTable,self).__init__(mark_as_completed)
        self.params = params
        self.ps_table = None

    def initialize(self):
        if self.dependency_inventory:
            self.dependency_inventory.add_dependent_resource(resource_name='th1_events',
                                        access_path = ['experiments','th1','events'])
            self.dependency_inventory.add_dependent_resource(resource_name='ps_events',
                                        access_path = ['experiments','ps','events'])
            self.dependency_inventory.add_dependent_resource(resource_name='bipolar',
                                        access_path = ['electrodes','bipolar'])

    def restore(self):
        subject = self.pipeline.subject
        experiment = self.pipeline.experiment
        self.ps_table = pd.read_pickle(self.get_path_to_resource_in_workspace(subject+'-'+experiment+'-ps_table.pkl'))
        self.pass_object('ps_table', self.ps_table)

    def run(self):
        subject = self.pipeline.subject
        experiment = self.pipeline.experiment

        ps_events = self.get_passed_object(experiment+'_events')
        loc_tag = self.get_passed_object('loc_tag')

        lr_classifier = self.get_passed_object('lr_classifier')
        xval_output = self.get_passed_object('xval_output')

        ps_pow_mat_pre = self.get_passed_object('ps_pow_mat_pre')
        ps_pow_mat_post = self.get_passed_object('ps_pow_mat_post')

        n_events = len(ps_events)

        prob_pre, prob_diff = self.compute_prob_deltas(ps_pow_mat_pre, ps_pow_mat_post, lr_classifier)

        probs = xval_output[-1].probs
        true_labels = xval_output[-1].true_labels
        performance_map = sorted(zip(probs,true_labels))
        probs, true_labels = zip(*performance_map)
        true_labels = np.array(true_labels)
        total_recall_performance = np.sum(true_labels) / float(len(true_labels))

        # the code below is not pythonic, but I'll figure it out later
        perf_diff = np.zeros(n_events, dtype=float)
        for i in xrange(n_events):
            #perf_pre = prob2perf(probs, true_labels, prob_pre[i]+1e-7)
            #perf_diff[i] = 100.0*(prob2perf(probs, true_labels, prob_pre[i]+prob_diff[i]+1e-7) - perf_pre) / total_recall_performance
            perf_pre = prob2perf_norm(xval_output[-1], prob_pre[i])
            perf_diff[i] = 100.0*(prob2perf_norm(xval_output[-1], prob_pre[i]+prob_diff[i]) - perf_pre) / total_recall_performance

        #define region
        bipolar_label = pd.Series(zip([s.upper() for s in ps_events.stimAnodeTag], [s.upper() for s in ps_events.stimCathodeTag]))
        region = bipolar_label.apply(lambda bp: bipolar_label_to_loc_tag(bp, loc_tag))

        self.ps_table = pd.DataFrame()
        self.ps_table['session'] = ps_events.session
        self.ps_table['mstime'] = ps_events.mstime
        self.ps_table['Pulse_Frequency'] = ps_events.pulse_frequency
        self.ps_table['Amplitude'] = ps_events.amplitude
        self.ps_table['Duration'] = ps_events.pulse_duration
        self.ps_table['Burst_Frequency'] = ps_events.burst_frequency
        self.ps_table['stimAnodeTag'] = ps_events.stimAnodeTag
        self.ps_table['stimCathodeTag'] = ps_events.stimCathodeTag
        self.ps_table['Region'] = region
        self.ps_table['prob_pre'] = prob_pre
        self.ps_table['prob_diff'] = prob_diff
        self.ps_table['perf_diff'] = perf_diff
        self.ps_table['isi'] = ps_events.isi
        
        self.pass_object('ps_table', self.ps_table)
        self.ps_table.to_pickle(self.get_path_to_resource_in_workspace(subject+'-'+experiment+'-ps_table.pkl'))

    def compute_prob_deltas(self, ps_pow_mat_pre, ps_pow_mat_post, lr_classifier):
        prob_pre = lr_classifier.predict_proba(ps_pow_mat_pre)[:,1]
        prob_post = lr_classifier.predict_proba(ps_pow_mat_post)[:,1]
        return prob_pre, prob_post - prob_pre