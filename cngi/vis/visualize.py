#   Copyright 2019 AUI, Inc. Washington DC, USA
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


def visualize(xda, axis=None, tsize=250):
    """
    Plot a preview of any xarray DataArray contents

    Parameters
    ----------
    xda : xarray.core.dataarray.DataArray
        input DataArray
    axis : str or list
        DataArray coordinate(s) to plot against data. Default None uses range
    tsize : int
        target size of the preview plot (might be smaller). Default is 250 points per axis

    Returns
    -------
      Open matplotlib window
    """
    import matplotlib.pyplot as plt
    import xarray
    import numpy as np
    import dask.array as da
    from pandas.plotting import register_matplotlib_converters
    register_matplotlib_converters()

    plt.clf()

    # fast decimate to roughly the desired size
    thinf = int(np.ceil(np.max(xda.shape[0])/tsize))
    txda = xda.thin(thinf)

    # can't plot complex numbers or bools (sometimes)
    if txda.dtype == 'complex128':
        txda = da.absolute(txda)
    elif txda.dtype == 'bool':
        txda = txda.astype(int)

    # default pcolormesh plot axes
    if (txda.ndim > 1) and (axis is None):
        axis = np.array(txda.dims[:2])
        if 'chan' in txda.dims: axis[-1] = 'chan'

    # collapse data to 1-D or 2-D
    if axis is not None:
        axis = np.atleast_1d(axis)
        if txda.ndim > 1:
            txda = txda.max(dim=[dd for dd in txda.dims if dd not in axis])
    
    # different types of plots depending on shape and parameters
    if (txda.ndim == 1) and (axis is None):
        pxda = xarray.DataArray(np.arange(len(txda)), dims=[txda.name], coords={txda.name:txda.values})
        pxda.plot.line(y=pxda.dims[0], marker='.', linewidth=0.0)
        plt.title(txda.name)
    elif (txda.ndim == 1):
        txda.plot.line(x=axis[0], marker='.', linewidth=0.0)
        plt.title(txda.name + ' vs ' + axis[0])
    else:  # more than 1-D
        txda.plot.pcolormesh(x=axis[0], y=axis[1])
        plt.title(txda.name + ' ' + axis[1] + ' vs ' + axis[0])