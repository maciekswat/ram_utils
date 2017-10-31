import os
from random import shuffle
import warnings
import hashlib

import numpy as np
from scipy.stats.mstats import zscore

from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from sklearn.metrics import roc_auc_score

from ptsa.data.readers.IndexReader import JsonIndexReader

from ReportTasks.RamTaskMethods import run_lolo_xval,run_loso_xval,permuted_loso_AUCs,permuted_lolo_AUCs,ModelOutput
from ReportUtils import ReportRamTask
from ramutils.classifier.utils import normalize_sessions, get_sample_weights


class ComputeClassifier(ReportRamTask):
    def __init__(self, params, mark_as_completed=True):
        super(ComputeClassifier,self).__init__(mark_as_completed)
        self.params = params
        self.pow_mat = None
        self.lr_classifier = None
        self.xval_output = dict()   # ModelOutput per session; xval_output[-1] is across all sessions
        self.perm_AUCs = None
        self.pvalue = None

    def input_hashsum(self):
        subject = self.pipeline.subject
        tmp = subject.split('_')
        subj_code = tmp[0]
        montage = 0 if len(tmp)==1 else int(tmp[1])

        json_reader = JsonIndexReader(os.path.join(self.pipeline.mount_point, 'protocols','r1.json'))

        hash_md5 = hashlib.md5()

        bp_paths = json_reader.aggregate_values('pairs', subject=subj_code, montage=montage)
        for fname in bp_paths:
            with open(fname,'rb') as f: hash_md5.update(f.read())

        fr1_event_files = sorted(list(json_reader.aggregate_values('all_events', subject=subj_code, montage=montage, experiment='FR1')))
        for fname in fr1_event_files:
            with open(fname,'rb') as f: hash_md5.update(f.read())

        catfr1_event_files = sorted(list(json_reader.aggregate_values('all_events', subject=subj_code, montage=montage, experiment='catFR1')))
        for fname in catfr1_event_files:
            with open(fname,'rb') as f: hash_md5.update(f.read())

        return hash_md5.digest()

    def xval_test_type(self, events):
        event_sessions = events.session
        sessions = np.unique(event_sessions)
        if len(sessions) == 1:
            return 'lolo'
        for sess in sessions:
            sess_events = events[event_sessions == sess]
            if len(sess_events) >= 0.7 * len(events):
                return 'lolo'
        return 'loso'

    @property
    def events(self):
        self._events = self.get_passed_object(self.pipeline.task+'_events')
        return self._events[self._events.type=='WORD']

    def _normalize_sessions(self,events):
        self.pow_mat = normalize_sessions(self.pow_mat, events)

    def get_pow_mat(self):
        events = self.events
        return self.get_passed_object('pow_mat')[self._events.type=='WORD',...]

    def run(self):
        subject = self.pipeline.subject

        events = self.events
        self.pow_mat = self.get_pow_mat()
        self._normalize_sessions(events)

        self.lr_classifier = LogisticRegression(C=self.params.C,
                                                penalty=self.params.penalty_type,
                                                class_weight='balanced',
                                                solver='liblinear')

        event_sessions = events.session
        recalls = events.recalled

        if self.xval_test_type(events) == 'loso':
            print 'Performing permutation test'
            self.perm_AUCs = permuted_loso_AUCs(self,event_sessions, recalls)

            print 'Performing leave-one-session-out xval'
            run_loso_xval(event_sessions, recalls,
                                        self.pow_mat, self.lr_classifier,self.xval_output,permuted=False)
        else:
            print 'Performing in-session permutation test'
            self.perm_AUCs = permuted_lolo_AUCs(self,events)

            print 'Performing leave-one-list-out xval'
            run_lolo_xval(events, recalls, self.pow_mat,self.lr_classifier,self.xval_output, permuted=False)

        self.pvalue = np.sum(self.perm_AUCs >= self.xval_output[-1].auc) / float(self.perm_AUCs.size)
        print 'Perm test p-value =', self.pvalue

        print 'thresh =', self.xval_output[-1].jstat_thresh, 'quantile =', self.xval_output[-1].jstat_quantile

        print 'AUC = ',self.xval_output[-1].auc

        # Finally, fitting classifier on all available data
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lr_classifier.fit(self.pow_mat, recalls)

        self.pass_objects()

    def pass_objects(self):

        subject=self.pipeline.subject
        self.pass_object('lr_classifier', self.lr_classifier)
        self.pass_object('xval_output', self.xval_output)
        self.pass_object('perm_AUCs', self.perm_AUCs)
        self.pass_object('pvalue', self.pvalue)

        joblib.dump(self.lr_classifier, self.get_path_to_resource_in_workspace(subject + '-lr_classifier.pkl'))
        joblib.dump(self.xval_output, self.get_path_to_resource_in_workspace(subject + '-xval_output.pkl'))
        joblib.dump(self.perm_AUCs, self.get_path_to_resource_in_workspace(subject + '-perm_AUCs.pkl'))
        joblib.dump(self.pvalue, self.get_path_to_resource_in_workspace(subject + '-pvalue.pkl'))

    def restore(self):
        subject = self.pipeline.subject
        task = self.pipeline.task

        for attr in ['lr_classifier','xval_output','perm_AUCs','pvalue']:
            try:
                self.__setattr__(attr,joblib.load(self.get_path_to_resource_in_workspace(subject + '-%s.pkl'%attr)))
            except IOError:
                self.__setattr__(attr,joblib.load(self.get_path_to_resource_in_workspace(subject + '-'+task+'-%s.pkl'%attr)))

        self.pass_object('lr_classifier', self.lr_classifier)
        self.pass_object('xval_output', self.xval_output)
        self.pass_object('perm_AUCs', self.perm_AUCs)
        self.pass_object('pvalue', self.pvalue)


class ComputeJointClassifier(ReportRamTask):

    def __init__(self, params, mark_as_completed=True):
        super(ComputeJointClassifier,self).__init__(mark_as_completed)
        self.params = params
        self.pow_mat = None
        self.lr_classifier = None
        self.xval_output = dict()   # ModelOutput per session; xval_output[-1] is across all sessions
        self.perm_AUCs = None
        self.pvalue = None

    def input_hashsum(self):
        subject = self.pipeline.subject
        tmp = subject.split('_')
        subj_code = tmp[0]
        montage = 0 if len(tmp)==1 else int(tmp[1])

        json_reader = JsonIndexReader(os.path.join(self.pipeline.mount_point, 'protocols','r1.json'))

        hash_md5 = hashlib.md5()

        bp_paths = json_reader.aggregate_values('pairs', subject=subj_code, montage=montage)
        for fname in bp_paths:
            with open(fname,'rb') as f: hash_md5.update(f.read())

        fr1_event_files = sorted(list(json_reader.aggregate_values('all_events', subject=subj_code, montage=montage, experiment='FR1')))
        for fname in fr1_event_files:
            with open(fname,'rb') as f: hash_md5.update(f.read())

        catfr1_event_files = sorted(list(json_reader.aggregate_values('all_events', subject=subj_code, montage=montage, experiment='catFR1')))
        for fname in catfr1_event_files:
            with open(fname,'rb') as f: hash_md5.update(f.read())

        return hash_md5.digest()

    def run(self):
        subject = self.pipeline.subject
        events = self.events
        self.pow_mat = self.get_pow_mat()
        encoding_mask = events.type=='WORD'
        self.pow_mat[encoding_mask] = normalize_sessions(self.pow_mat[encoding_mask],events[encoding_mask])
        self.pow_mat[~encoding_mask] = normalize_sessions(self.pow_mat[~encoding_mask],events[~encoding_mask])

        # Save this power matrix for debugging
        self.save_array_to_hdf5(self.get_path_to_resource_in_workspace(subject + "-debug_data.h5"),
                                "norm_pow_mat",
                                self.pow_mat)
        self.save_array_to_hdf5(self.get_path_to_resource_in_workspace(subject + '-debug_data.h5'),
                                "recall",
                                events.recalled)

        self.lr_classifier = LogisticRegression(C=self.params.C,
                                                penalty=self.params.penalty_type,
                                                solver='liblinear',
                                                fit_intercept=True)

        event_sessions = events.session

        recalls = events.recalled
        recalls[events.type=='REC_WORD'] = 1
        recalls[events.type=='REC_BASE'] = 0

        sample_weights = get_sample_weights(events, self.params.encoding_samples_weight)

        sessions = np.unique(event_sessions)
        if len(sessions) > 1:
            print 'Performing permutation test'
            self.perm_AUCs = self.permuted_loso_AUCs(event_sessions, recalls, sample_weights,events=events)

            print 'Performing leave-one-session-out xval'
            self.run_loso_xval(event_sessions, recalls, permuted=False,samples_weights=sample_weights, events=events)
        else:
            sess = sessions[0]
            event_lists = events.list

            print 'Performing in-session permutation test'
            self.perm_AUCs = self.permuted_lolo_AUCs(sess, event_lists, recalls,samples_weights=sample_weights)

            print 'Performing leave-one-list-out xval'
            self.run_lolo_xval(sess, event_lists, recalls, permuted=False,samples_weights=sample_weights)

        print 'CROSS VALIDATION ENCODING AUC =', self.xval_output[-1].auc

        self.pvalue = np.nansum(self.perm_AUCs >= self.xval_output[-1].auc) / float(self.perm_AUCs[~np.isnan(self.perm_AUCs)].size)
        print 'Perm test p-value =', self.pvalue

        print 'thresh =', self.xval_output[-1].jstat_thresh, 'quantile =', self.xval_output[-1].jstat_quantile

        self.lr_classifier.fit(self.pow_mat, recalls, sample_weights)

        # Save predicted probabilities and model weights
        model_output = self.lr_classifier.predict_proba(self.pow_mat)[:, 1]
        model_weights = self.lr_classifier.coef_
        self.save_array_to_hdf5(self.get_path_to_resource_in_workspace(subject + "-debug_data.h5"),
                                "model_output",
                                model_output)
        self.save_array_to_hdf5(self.get_path_to_resource_in_workspace(subject + "-debug_data.h5"),
                                "model_weights",
                                model_weights)

        self.pass_objects()

    @property
    def events(self):
        self._events = self.get_passed_object(self.pipeline.task+'_events')
        return self._events

    def get_pow_mat(self):
        return self.get_passed_object('pow_mat')

    def _normalize_sessions(self,events):
        encoding_mask = events.type=='WORD'
        self.pow_mat[encoding_mask]= normalize_sessions(self.pow_mat[encoding_mask],events[encoding_mask])
        self.pow_mat[~encoding_mask] = normalize_sessions(self.pow_mat[~encoding_mask],events[~encoding_mask])

    def pass_objects(self):
        subject = self.pipeline.subject
        self.pass_object('joint_lr_classifier', self.lr_classifier)
        self.pass_object('joint_xval_output', self.xval_output)
        self.pass_object('joint_perm_AUCs', self.perm_AUCs)
        self.pass_object('joint_pvalue', self.pvalue)

        joblib.dump(self.lr_classifier, self.get_path_to_resource_in_workspace(subject +    '-joint_lr_classifier.pkl'))
        joblib.dump(self.xval_output, self.get_path_to_resource_in_workspace(subject +      '-joint_xval_output.pkl'))
        joblib.dump(self.perm_AUCs, self.get_path_to_resource_in_workspace(subject +        '-joint_perm_AUCs.pkl'))
        joblib.dump(self.pvalue, self.get_path_to_resource_in_workspace(subject +           '-joint_pvalue.pkl'))

    def run_loso_xval(self, event_sessions, recalls, permuted=False,samples_weights=None, events=None):
        probs = np.empty_like(events[events.type=='WORD'], dtype=np.float)

        sessions = np.unique(event_sessions)

        auc_encoding = np.empty(sessions.shape[0], dtype=np.float)
        auc_retrieval = np.empty(sessions.shape[0], dtype=np.float)
        auc_both = np.empty(sessions.shape[0], dtype=np.float)

        for sess_idx, sess in enumerate(sessions):
            insample_mask = (event_sessions != sess)
            insample_pow_mat = self.pow_mat[insample_mask]
            insample_recalls = recalls[insample_mask]
            insample_samples_weights = get_sample_weights(events[events.session != sess],
                                                          self.params.encoding_samples_weight)
            outsample_both_mask = (events.session == sess)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                if samples_weights is not None:
                    self.lr_classifier.fit(insample_pow_mat,
                                           insample_recalls,
                                           insample_samples_weights)
                else:
                    self.lr_classifier.fit(insample_pow_mat, insample_recalls)

            outsample_mask = (~insample_mask) & (events.type=='WORD')
            outsample_pow_mat = self.pow_mat[outsample_mask]
            outsample_recalls = recalls[outsample_mask]

            outsample_probs = self.lr_classifier.predict_proba(outsample_pow_mat)[:, 1]
            if not permuted:
                self.xval_output[sess] = ModelOutput(outsample_recalls, outsample_probs)
                self.xval_output[sess].compute_roc()
                self.xval_output[sess].compute_tercile_stats()
            probs[events[events.type=='WORD'].session==sess] = outsample_probs


            if events is not None:

                outsample_encoding_mask = (events.session == sess) & (events.type == 'WORD')
                outsample_retrieval_mask = (events.session == sess) & ((events.type == 'REC_BASE') | (events.type == 'REC_WORD'))
                outsample_both_mask = (events.session == sess)

                auc_encoding[sess_idx] = self.get_auc(
                    classifier=self.lr_classifier, features=self.pow_mat, recalls=recalls, mask=outsample_encoding_mask)

                auc_retrieval[sess_idx] = self.get_auc(
                    classifier=self.lr_classifier, features=self.pow_mat, recalls=recalls, mask=outsample_retrieval_mask)

                auc_both[sess_idx] = self.get_auc(
                    classifier=self.lr_classifier, features=self.pow_mat, recalls=recalls, mask=outsample_both_mask)

        if not permuted:
            self.xval_output[-1] = ModelOutput(recalls[events.type=='WORD'], probs)
            self.xval_output[-1].compute_roc()
            self.xval_output[-1].compute_tercile_stats()
            print 'auc_encoding=',auc_encoding, np.mean(auc_encoding)
            print 'auc_retrieval=',auc_retrieval, np.mean(auc_retrieval)
            print 'auc_both=',auc_both, np.mean(auc_both)

        return probs

    def get_auc(self, classifier, features, recalls, mask):

        masked_recalls = recalls[mask]
        probs = classifier.predict_proba(features[mask])[:, 1]
        auc = roc_auc_score(masked_recalls, probs)
        return auc

    def permuted_loso_AUCs(self, event_sessions, recalls, samples_weights=None,events=None):
        n_perm = self.params.n_perm
        permuted_recalls = np.array(recalls)
        AUCs = np.empty(shape=n_perm, dtype=np.float)
        for i in xrange(n_perm):
            try:
                for sess in event_sessions:
                    sel = (event_sessions == sess)
                    sess_permuted_recalls = permuted_recalls[sel]
                    shuffle(sess_permuted_recalls)
                    permuted_recalls[sel] = sess_permuted_recalls
                probs = self.run_loso_xval(event_sessions, permuted_recalls, permuted=True,samples_weights=samples_weights,events=events)
                AUCs[i] = roc_auc_score(recalls[events.type=='WORD'], probs)
                print 'AUC =', AUCs[i]
            except ValueError:
                AUCs[i] = np.nan
        return AUCs

    def run_lolo_xval(self, sess, event_lists, recalls, permuted=False, samples_weights=None):
        probs = np.empty_like(recalls, dtype=np.float)

        lists = np.unique(event_lists)

        for lst in lists:
            insample_mask = (event_lists != lst)
            insample_pow_mat = self.pow_mat[insample_mask]
            insample_recalls = recalls[insample_mask]
            insample_samples_weights = samples_weights[insample_mask]

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                if samples_weights is not None:
                    self.lr_classifier.fit(insample_pow_mat, insample_recalls,insample_samples_weights)
                else:
                    self.lr_classifier.fit(insample_pow_mat, insample_recalls)


            outsample_mask = ~insample_mask
            outsample_pow_mat = self.pow_mat[outsample_mask]

            probs[outsample_mask] = self.lr_classifier.predict_proba(outsample_pow_mat)[:, 1]

        if not permuted:
            xval_output = ModelOutput(recalls, probs)
            xval_output.compute_roc()
            xval_output.compute_tercile_stats()
            self.xval_output[sess] = self.xval_output[-1] = xval_output

        return probs

    def permuted_lolo_AUCs(self, sess, event_lists, recalls,samples_weights=None):
        n_perm = self.params.n_perm
        permuted_recalls = np.array(recalls)
        AUCs = np.empty(shape=n_perm, dtype=np.float)
        for i in xrange(n_perm):
            for lst in event_lists:
                sel = (event_lists == lst)
                list_permuted_recalls = permuted_recalls[sel]
                shuffle(list_permuted_recalls)
                permuted_recalls[sel] = list_permuted_recalls
            probs = self.run_lolo_xval(sess, event_lists, permuted_recalls, permuted=True,samples_weights=samples_weights)
            AUCs[i] = roc_auc_score(recalls, probs)
            print 'AUC =', AUCs[i]
        return AUCs

    def restore(self):
        subject = self.pipeline.subject

        for attr in ['lr_classifier','xval_output','perm_AUCs','pvalue']:
            self.__setattr__(attr,joblib.load(self.get_path_to_resource_in_workspace(subject + '-joint_%s.pkl'%attr)))

        self.pass_object('joint_lr_classifier', self.lr_classifier)
        self.pass_object('joint_xval_output', self.xval_output)
        self.pass_object('joint_perm_AUCs', self.perm_AUCs)
        self.pass_object('joint_pvalue', self.pvalue)
