import functools
import numpy as np
import pandas as pd
from pkg_resources import resource_filename
import warnings

import pytest

from numpy.testing import assert_equal, assert_almost_equal

from traits.api import ListInt, ListFloat, ListBool

from ramutils.reports.summary import *
from ramutils.tasks.events import build_ps_data
from ramutils.events import  extract_biomarker_information
datafile = functools.partial(resource_filename, 'ramutils.test.test_data')


def _fr5_events():
    """FR5 events for R1345D."""
    filename = datafile('fr5-events.npz')
    events = np.rec.array(np.load(filename)['events'])
    return events[events.session == 0]


def _ticlfr_events():
    """TICL_FR events for R1427T"""
    filename = datafile('ticl_fr_events.npz')
    events = np.rec.array(np.load(filename)['events'])
    return events


@pytest.fixture(scope='session')
def math_events():
    """Math events for all FR1 sessions of R1111M."""
    filename = datafile('R1111M_math_events.npz')
    events = np.rec.array(np.load(filename)['events'])
    return events


def _bipolar_pairs():
    return {}


def _excluded_pairs():
    return {}


def _normalized_powers():
    return np.array([[1, 2], [3, 4]])

fr5_events = pytest.fixture(scope='session')(_fr5_events)
ticlfr_events = pytest.fixture(scope='session')(_ticlfr_events)
bipolar_pairs = pytest.fixture(scope='session')(_bipolar_pairs)
excluded_pairs = pytest.fixture(scope='session')(_excluded_pairs)
normalized_powers = pytest.fixture(scope='session')(_normalized_powers)


@pytest.fixture()
def ps_events(rhino_root):
    ps_events = build_ps_data('R1364C', 'PS4_FR', 'ps4_events', None,
                              rhino_root)
    return ps_events


class TestSummary:
    def test_to_dataframe(self, fr5_events, bipolar_pairs, excluded_pairs,
                          normalized_powers):

        summary = SessionSummary()
        summary.populate(fr5_events, bipolar_pairs,
                         excluded_pairs, normalized_powers)
        df = summary.to_dataframe()
        assert len(df) == len(fr5_events)

    def test_session_length(self, fr5_events):
        summary = SessionSummary()
        summary.events = fr5_events
        assert np.floor(summary.session_length) == 2475

    def test_session_datetime(self, fr5_events):
        summary = SessionSummary()
        summary.events = fr5_events
        dt = summary.session_datetime
        assert dt.tzinfo is not None
        assert dt.year == 2017
        assert dt.month == 10
        assert dt.day == 9
        assert dt.hour == 18
        assert dt.minute == 8
        assert dt.second == 25
        assert dt.utcoffset().total_seconds() == 0

    def test_populate(self):
        with pytest.raises(NotImplementedError):
            summary = Summary()
            summary.populate(None, None, None, None)

    def test_create(self, fr5_events, bipolar_pairs, excluded_pairs,
                    normalized_powers):
        summary = SessionSummary.create(fr5_events, bipolar_pairs,
                                        excluded_pairs, normalized_powers)
        assert_equal(summary.events, fr5_events)


class TestMathSummary:
    @classmethod
    def setup_class(cls):
        # ignore UserWarnings from summaries.populate calls
        warnings.filterwarnings('ignore', category=UserWarning)

    @classmethod
    def teardown_class(cls):
        warnings.resetwarnings()

    @staticmethod
    def all_summaries(events):
        summaries = []
        for session in np.unique(events.session):
            summary = MathSummary()
            summary.populate(events[events.session == session])
            summaries.append(summary)
        return summaries

    def test_num_problems(self, math_events):
        probs = 0
        for session in np.unique(math_events.session):
            events = math_events[math_events.session == session]
            summary = MathSummary()
            summary.populate(events)
            probs += summary.num_problems

        assert probs == 286

    def test_num_correct(self, math_events):
        correct = 0
        for session in np.unique(math_events.session):
            events = math_events[math_events.session == session]
            summary = MathSummary()
            summary.populate(events)
            correct += summary.num_correct

        assert correct == 260

    def test_percent_correct(self, math_events):
        percents = []
        for session in np.unique(math_events.session):
            events = math_events[math_events.session == session]
            summary = MathSummary()
            summary.populate(events)
            percents.append(summary.percent_correct)

        assert_almost_equal(percents, [95, 92, 91, 87], decimal=0)

    def test_problems_per_list(self, math_events):
        ppl = []
        for session in np.unique(math_events.session):
            events = math_events[math_events.session == session]
            summary = MathSummary()
            summary.populate(events)
            ppl.append(summary.problems_per_list)

        assert_almost_equal(ppl, [3.33, 3.0, 2.96, 4.2], decimal=2)

    def test_total_num_problems(self, math_events):
        summaries = self.all_summaries(math_events)
        assert MathSummary.total_num_problems(summaries) == 286

    def test_total_num_correct(self, math_events):
        summaries = self.all_summaries(math_events)
        assert MathSummary.total_num_correct(summaries) == 260

    def test_total_percent_correct(self, math_events):
        summaries = self.all_summaries(math_events)
        assert np.floor(MathSummary.total_percent_correct(summaries)) == 90

    def test_total_problems_per_list(self, math_events):
        summaries = self.all_summaries(math_events)

        # FIXME: the existing R1111M FR1 report says this should be 3.62
        assert_almost_equal([MathSummary.total_problems_per_list(summaries)],
                            [3.36], decimal=2)


class TestFRSessionSummary:
    @classmethod
    def setup_class(cls):
        cls.summary = FRSessionSummary()
        events = _fr5_events()
        pairs = _bipolar_pairs()
        excluded = _excluded_pairs()
        powers = _normalized_powers()
        cls.summary.populate(events, pairs, excluded, powers)

    def test_num_lists(self):
        assert self.summary.num_lists == 25

    def test_percent_recalled(self):
        assert self.summary.percent_recalled == 16

    @pytest.mark.parametrize('first', [True, False])
    def test_serialpos_probabilities(self, first):
        if first:
            expected = [0.2, 0.12, 0.08, 0.08, 0.08,
                        0.0, 0.08, 0.04, 0.08, 0.0, 0.0, 0.04]
        else:
            expected = [0.2, 0.16, 0.08, 0.16, 0.16,
                        0.12, 0.28, 0.2, 0.08, 0.16, 0.24, 0.08]

        probs = FRSessionSummary.serialpos_probabilities([self.summary], first)
        assert_almost_equal(probs, expected, decimal=2)


class TestCatFRSessionSummary:
    @classmethod
    def setup_class(cls):
        cls.summary = CatFRSessionSummary()
        events = _fr5_events()
        raw_events = _fr5_events()
        pairs = _bipolar_pairs()
        excluded = _excluded_pairs()
        powers = _normalized_powers()
        cls.summary.populate(events, pairs, excluded,
                             powers, raw_events=raw_events)

    def test_to_dataframe(self):
        df = self.summary.to_dataframe()
        assert len(df) == len(self.summary.events)


class TestStimSessionSummary:
    @pytest.mark.parametrize('is_ps4_session', [True, False])
    def test_populate(self, fr5_events, bipolar_pairs, excluded_pairs,
                      normalized_powers):
        """Basic tests that data was populated correctly from events."""
        summary = StimSessionSummary()
        summary.populate(fr5_events, bipolar_pairs,
                         excluded_pairs, normalized_powers)
        df = summary.to_dataframe()

        assert len(df[df.phase == 'BASELINE']) == 36
        assert len(df[df.phase == 'STIM']) == 192
        assert len(df[df.phase == 'NON-STIM']) == 72


class TestClassifierSummary:
    @classmethod
    def setup_class(cls):
        cls.subject = 'TEST_SUBJECT'
        cls.experiment = 'TEST'
        cls.sessions = ['NA']
        cls.recalls = np.random.randint(0, 2, 100)
        cls.predicted_probabilities = np.random.normal(.5, .03, size=100)
        cls.permuation_aucs = np.random.normal(.5, .01, size=200)
        cls.freqs = np.arange(10)
        cls.pairs = np.array(['A1','A2','A3'])
        cls.coef =  np.random.rand(1,len(cls.freqs)*len(cls.pairs))
        cls.features = np.random.rand(10,cls.coef.shape[-1])
        cls.summary = ClassifierSummary()

    def test_populate(self):
        summary = ClassifierSummary()
        summary.populate(self.subject, self.experiment, self.sessions,
                         self.recalls, self.predicted_probabilities,
                         self.permuation_aucs,
                         self.freqs,self.pairs,self.features,self.coef,
                         tag='Encoding')
        assert np.array_equal(self.recalls, summary.true_outcomes)
        assert np.array_equal(self.predicted_probabilities,
                              summary.predicted_probabilities)
        assert np.array_equal(self.permuation_aucs,
                              summary.permuted_auc_values)
        assert summary.tag == 'Encoding'
        assert summary.reloaded == False

        return

    def test_auc(self):
        summary = ClassifierSummary()
        summary.populate(self.subject, self.experiment, self.sessions,
                         self.recalls, self.predicted_probabilities,
                         self.permuation_aucs,
                         self.freqs, self.pairs, self.features, self.coef)
        return

    def test_pvalue(self):
        pass

    def test_false_positive_rate(self):
        pass

    def test_true_positive_rate(self):
        pass

    def test_thresholds(self):
        pass

    def test_median_classifier_output(self):
        pass

    def test_low_tercile_diff_from_mean(self):
        pass

    def test_high_tercile_diff_from_mean(self):
        pass


class TestStimSessionSummary:
    @classmethod
    def setup_class(cls):
        cls.sample_summary_table = pd.read_csv(datafile(
            "/input/summaries/sample_stim_session_summary.csv"))


class TestTiclFRSessionSummary:
    @classmethod
    def setup_class(cls):
        cls.events = _ticlfr_events()
        cls.sample_summary = TICLFRSessionSummary()
        cls.sample_summary.raw_events = cls.events
        cls.sample_summary.biomarker_events = extract_biomarker_information(
            cls.events)

    @pytest.mark.parametrize("phase", ["ENCODING", "DISTRACT", "RETRIEVAL"])
    def test_nstims(self, phase):
        assert self.sample_summary.nstims(phase) > 0

    @pytest.mark.parametrize("phase", ["ENCODING", "DISTRACT", "RETRIEVAL"])
    @pytest.mark.parametrize("position", ["pre", "post"])
    def test_classifier_output(self,phase, position):
        output_list = self.sample_summary.classifier_output(phase,position)
        assert len(output_list) > 0
        assert all(x >= 0 for x in output_list)

    @pytest.mark.parametrize("phase", ["ENCODING", "DISTRACT", "RETRIEVAL", None])
    def test_pre_stim_prob_recall(self, phase):
        output_list = TICLFRSessionSummary.pre_stim_prob_recall(
            [self.sample_summary], phase)
        assert len(output_list) > 0
        assert all(x >= 0 for x in output_list)
        assert len(output_list) == len(TICLFRSessionSummary.all_post_stim_prob_recall(
            [self.sample_summary], phase
        ))

    @pytest.mark.parametrize("phase",
                             ["ENCODING", "DISTRACT", "RETRIEVAL", None])
    def test_post_stim_prob_recall(self,phase):
        output_list = TICLFRSessionSummary.all_post_stim_prob_recall(
            [self.sample_summary], phase
        )

        assert len(output_list) > 0
        assert all(x >= 0 for x in output_list)


class TestFRStimSessionSummary:
    @classmethod
    def setup_class(cls):
        cls.sample_summary_table = pd.read_csv(datafile(
            "/input/summaries/sample_stim_session_summary.csv"))
        cls.sample_events = cls.sample_summary_table.to_records(index=False)
        cls.sample_summary = FRStimSessionSummary()
        pairs = _bipolar_pairs()
        excluded = _excluded_pairs()
        powers = _normalized_powers()
        cls.sample_summary.populate(cls.sample_events, pairs, excluded, powers)

    def test_num_nonstim_lists(self):
        assert FRStimSessionSummary.num_nonstim_lists(
            [self.sample_summary]) == 9

    def test_num_stim_lists(self):
        assert FRStimSessionSummary.num_stim_lists([self.sample_summary]) == 16

    def test_lists(self):
        lists = FRStimSessionSummary.lists([self.sample_summary])
        assert min(lists) == 1
        assert max(lists) == 25

        stim_lists = FRStimSessionSummary.lists(
            [self.sample_summary], stim=True)
        assert len(stim_lists) == 16

    def test_stim_events_by_list(self):
        stim_events_by_list = FRStimSessionSummary.stim_events_by_list(
            [self.sample_summary])
        assert min(stim_events_by_list) == 0
        assert max(stim_events_by_list) == 9

    def test_prob_stim_by_serialpos(self):
        prob_stim_by_serialpos = FRStimSessionSummary.prob_stim_by_serialpos([
                                                                             self.sample_summary])
        assert min(prob_stim_by_serialpos) > .46
        assert max(prob_stim_by_serialpos) > .52
        return

    def test_recalls_by_list(self):
        stim_recalls_by_list = FRStimSessionSummary.recalls_by_list(
            [self.sample_summary], stim_list_only=True)
        assert sum(stim_recalls_by_list) == 43

        nonstim_recalls_by_list = FRStimSessionSummary.recalls_by_list(
            [self.sample_summary], stim_list_only=False)
        assert sum(nonstim_recalls_by_list) == 55

    def test_prob_first_recall_by_serialpos(self):
        prob_first_recall_nonstim = FRStimSessionSummary.prob_first_recall_by_serialpos(
            [self.sample_summary], stim=False)
        assert max(prob_first_recall_nonstim) < 0.57

        prob_first_recall_stim = FRStimSessionSummary.prob_first_recall_by_serialpos(
            [self.sample_summary], stim=True)
        assert max(prob_first_recall_stim) < 0.13

    def test_prob_recall_by_serialpos(self):
        recall_by_serialpos = FRStimSessionSummary.prob_recall_by_serialpos(
            [self.sample_summary],
            stim_items_only=False)
        assert max(recall_by_serialpos) > 0.29
        assert min(recall_by_serialpos) < 0.53

        recall_by_serialpos = FRStimSessionSummary.prob_recall_by_serialpos(
            [self.sample_summary],
            stim_items_only=True)
        assert max(recall_by_serialpos) > 0.66
        assert min(recall_by_serialpos) == 0

    def test_delta_recall(self):
        delta_recall_stim = FRStimSessionSummary.delta_recall(
            [self.sample_summary],
            post_stim_items=False)
        assert np.isclose(delta_recall_stim, 52.931805334)

        delta_recall_post_stim = FRStimSessionSummary.delta_recall(
            [self.sample_summary],
            post_stim_items=True)
        assert np.isclose(delta_recall_post_stim, 32.4731351)

    def test_stim_parameters(self):
        stim_params = FRStimSessionSummary.stim_parameters(
            [self.sample_summary])
        assert len(stim_params) == 1

    def test_recall_test_results(self):
        test_results = FRStimSessionSummary.recall_test_results(
            [self.sample_summary], 'FR5')
        # TODO: Manually check these values to ensure accuracy and add
        # assertions


@pytest.mark.rhino
class TestPSSessionSummary:
    @classmethod
    def setup_class(cls):
        # Events file is too large to store in repo, so build it from scratch
        cls.sample_summary = PSSessionSummary()

    @pytest.mark.xfail(reason='PS Events to dataframe not implemented')
    def test_to_dataframe(self, ps_events, bipolar_pairs, excluded_pairs):
        self.sample_summary.populate(
            ps_events, bipolar_pairs, excluded_pairs, _normalized_powers)
        df = self.sample_summary.to_dataframe()
        assert len(df) == 3068

    def test_decision(self, ps_events, bipolar_pairs, excluded_pairs,
                      normalized_powers):
        self.sample_summary.populate(ps_events, bipolar_pairs, excluded_pairs,
                                     normalized_powers)
        decision = self.sample_summary.decision
        print(decision)
        assert decision['best_amplitude'] == 1.0
        assert decision['best_location'] == 'TOJ7_TOJ8'
        assert np.isclose(decision['pval'], 0.101613, 1e-3)

    def test_location_summary(self, ps_events, bipolar_pairs, excluded_pairs,
                              normalized_powers):
        self.sample_summary.populate(ps_events, bipolar_pairs, excluded_pairs,
                                     normalized_powers)
        location_summaries = self.sample_summary.location_summary
        assert np.isclose(location_summaries['TOJ7_TOJ8'][
                              'best_delta_classifier'], 0.0630465, 1e-3)
        assert np.isclose(location_summaries['HCB11_HCB12'][
                              'best_delta_classifier'], 0.08719, 1e-3)

