import pytest
import functools
import numpy as np

from pkg_resources import resource_filename
from ramutils.classifier.utils import reload_classifier, train_classifier


datafile = functools.partial(resource_filename,
                             'ramutils.test.test_data.input')


@pytest.mark.parametrize('subject', [
    'R1354E',
    'R1365N'
])
def test_reload_classifier(subject):
    container = reload_classifier(subject, 'task', '0', base_path=datafile(
        '/classifiers/{}/'.format(subject)))
    assert container.classifier is not None

    return


@pytest.mark.parametrize('subject', [
    'R1350D',
    'R1353N',
    'R1354E'
])
def test_train_classifier(subject):
    events = np.load(datafile('/events/{}_task_events.npy'.format(
        subject))).view(np.recarray)
    powers = np.load(datafile('/powers/{}_normalized_powers.npy'.format(
        subject)))
    weights = np.load(datafile('/weights/{}_sample_weights.npy'.format(
        subject)))

    trained_classifier = train_classifier(powers, events, weights, 0.001,
                                          'l2', 'liblinear')

    # TODO: Need some strong checks here
    assert trained_classifier is not None
    return