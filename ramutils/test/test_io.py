import pytest

import h5py
import numpy as np
from numpy.testing import assert_equal
from traits.api import Array
from traitschema import Schema

from ramutils.io import store_results, load_results


class MySchema(Schema):
    x = Array(dtype=np.float)
    y = Array(dtype=np.float)


@pytest.mark.parametrize("scheme", ['', 'file'])
@pytest.mark.parametrize("datatype", ['schema', 'array'])
def test_store_results(scheme, datatype, tmpdir):
    data = None
    x, y = np.random.random((100,)), np.random.random((100, 100))

    if datatype == 'array':
        data = np.random.random((100, 100))
    elif datatype == 'schema':
        data = MySchema(x=x, y=y)

    path = str(tmpdir.join('out.h5'))
    if scheme != '':
        uri = 'file://{:s}/out.h5'.format(str(tmpdir))
    else:
        uri = path

    if scheme in ['', 'file']:
        store_results(data, uri)

        with h5py.File(path, 'r') as hfile:
            if isinstance(data, np.ndarray):
                assert_equal(hfile['/data'], data)
            else:
                assert_equal(x, hfile['/x'])
                assert_equal(y, hfile['/y'])
    else:
        raise RuntimeError("not a valid scheme")

    # Invalid data type
    with pytest.raises(NotImplementedError):
        store_results([1, 2, 3], uri)

    # Invalid scheme
    with pytest.raises(NotImplementedError):
        store_results(data, 'sqlite:///path.sqlite')


@pytest.mark.parametrize('scheme', ['', 'file:///'])
def test_load_results(scheme, tmpdir):
    data = MySchema(x=np.array([1]), y=np.array([2]))
    path = str(tmpdir.join('out.h5'))
    data.to_hdf(path)
    url = "{:s}{:s}".format(scheme, path)

    results = load_results(url)

    assert results.x == data.x
    assert results.y == data.y
