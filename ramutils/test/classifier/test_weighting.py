import pytest
import functools
import numpy as np

from pkg_resources import resource_filename
from ramutils.parameters import FRParameters, PALParameters
from ramutils.utils import load_event_test_data
from ramutils.classifier.weighting import \
    determine_weighting_scheme_from_events, get_equal_weights, \
    get_fr_sample_weights, get_pal_sample_weights, get_sample_weights

datafile = functools.partial(resource_filename,
                             'ramutils.test.test_data.input')


@pytest.mark.parametrize("event_file, exp_scheme", [
    ('R1350D_task_events.npy', 'FR'),
    ('R1348J_task_events.npy', 'FR'),
    ('R1354E_task_events.npy', 'FR'),
    ('R1353N_task_events.npy', 'PAL')
])
def test_determine_weighting_scheme_from_events(event_file, exp_scheme,
                                                rhino_root):
    events = load_event_test_data(
        datafile('/events/' + event_file), rhino_root)
    scheme = determine_weighting_scheme_from_events(events)
    assert scheme == exp_scheme
    return


@pytest.mark.parametrize("event_file", [
    'R1350D_task_events.npy',
    'R1348J_task_events.npy',
    'R1353N_task_events.npy',
    'R1354E_task_events.npy'
])
def test_get_equal_weights(event_file, rhino_root):
    events = load_event_test_data(datafile('/events/' + event_file),
                                  rhino_root)
    weights = get_equal_weights(events)
    assert len(weights) == len(events)
    assert np.allclose(weights, 1)
    return


@pytest.mark.parametrize("event_file", [
    'R1350D_task_events.npy',
])
def test_force_specific_weighting(event_file, rhino_root):
    events = load_event_test_data(
        datafile('/events/' + event_file), rhino_root)
    weights = get_sample_weights(events, scheme='EQUAL')
    assert len(weights) == len(events)
    assert np.allclose(weights, 1)

    with pytest.raises(NotImplementedError):
        weights = get_sample_weights(events, scheme='NOT_IMPLEMENTED')

    return


@pytest.mark.parametrize("event_file", [
    'R1350D_task_events.npy',
    'R1348J_task_events.npy',
    'R1354E_task_events.npy'
])
def test_get_fr_sample_weights(event_file, rhino_root):
    # TODO: This check should be more robust
    events = load_event_test_data(
        datafile('/events/' + event_file), rhino_root)
    weights = get_fr_sample_weights(events, 2.5)
    assert np.allclose(weights, 1) == False
    return


@pytest.mark.parametrize("event_file", [
    'R1353N_task_events.npy'
])
def test_get_pal_sample_weights(event_file, rhino_root):
    # TODO: This check should be more robust
    events = load_event_test_data(datafile('/events/' + event_file),
                                  rhino_root)
    weights = get_pal_sample_weights(events, 7.2, 1.93)
    assert np.allclose(weights, 1) == False
    return


@pytest.mark.parametrize("event_file, parameters", [
    ('R1350D_task_events.npy', FRParameters),
    ('R1348J_task_events.npy', FRParameters),
    ('R1354E_task_events.npy', FRParameters),
    ('R1353N_task_events.npy', PALParameters)
])
def test_get_sample_weights_blackbox(event_file, parameters, rhino_root):
    parameters = parameters().to_dict()
    events = load_event_test_data(datafile('/events/' + event_file),
                                  rhino_root)
    weights = get_sample_weights(events, **parameters)

    assert np.allclose(weights, 1) == False

    return


@pytest.mark.parametrize("event_file, exp_weights, parameters", [
    ('R1350D_task_events.npy', 'R1350D_sample_weights.npy', FRParameters),
    ('R1348J_task_events.npy', 'R1348J_sample_weights.npy', FRParameters),
    ('R1354E_task_events.npy', 'R1354E_sample_weights.npy', FRParameters),
    ('R1353N_task_events.npy', 'R1353N_sample_weights.npy', PALParameters)
])
def test_sample_weighting_regression(event_file, exp_weights, parameters,
                                     rhino_root):
    parameters = parameters().to_dict()
    events = load_event_test_data(
        datafile('/events/' + event_file), rhino_root)
    current_weights = get_sample_weights(events, **parameters)
    old_weights = np.load(datafile('/weights/' + exp_weights))

    assert np.allclose(current_weights, old_weights)

    return
