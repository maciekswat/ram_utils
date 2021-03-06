from importlib import import_module

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

import h5py
import numpy as np
from traitschema import Schema


def store_results(data, url):
    """Put computed data into storage.

    Parameters
    ----------
    data
        Data to store. Valid types include :class:`traitschema.Schema` instances
        and Numpy arrays.
    url : str
        URI spec or file path for storing data.

    Notes
    -----
    The ``url`` parameter is intended to accept generic URIs for the future
    ability to store to other backends, meaning that the scheme component (the
    piece before ``://``) indicates how and where to store the data. By default,
    if ``url`` looks like a path, this function will assume it is just writing
    to disk. In other words, ``/tmp/output`` is equivalent to
    ``file:///tmp/output``.

    """
    url = urlparse(url)
    if url.scheme in ['file', '']:
        assert url.path.endswith('.h5'), "data must be saved as HDF5 files"
        if isinstance(data, Schema):
            data.to_hdf(url.path)
        elif isinstance(data, np.ndarray):
            print(url.path)
            with h5py.File(url.path, 'w') as hfile:
                hfile['/data'] = data
        else:
            raise NotImplementedError(
                "Data must be a numpy array or a Schema instance")
    else:
        raise NotImplementedError("Only filesystem storage is implemented.")


def load_results(url):
    """Load previously computed results from storage.

    Parameters
    ----------
    url : str
        URI spec or file path for storing data.

    Notes
    -----
    See also :func:`store_results`.


    """
    url = urlparse(url)
    if url.scheme in ['file', '']:
        with h5py.File(url.path, 'r') as hfile:
            # Saved object is a Schema instance
            if 'classname' in hfile.attrs:
                modname = hfile.attrs['python_module']
                mod = import_module(modname)
                cls = getattr(mod, hfile.attrs['classname'])
                return cls.from_hdf(url.path)

            # Saved object is a raw numpy array
            else:
                return hfile['/data'].value
    else:
        raise NotImplementedError("Only filesystem storage is implemented.")
