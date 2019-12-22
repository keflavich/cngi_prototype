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


def mask(xds, name='mask1', ra=None, dec=None, pixels=None, stokes=-1, channels=-1):
    """
    Create a new mask Data variable in the Dataset \n
    NOTE: currently only supports rectangles and integer pixel boundaries

    Parameters
    ----------
    xds : xarray Dataset
        input image dataset
    name : str
        dataset variable name for region, overwrites if already present
    ra : list
        right ascension coordinate range in the form of [min, max]. Default None means all
    dec : list
        declination coordinate range in the form of [min, max]. Default None means all
    pixels : numpy array
        array of shape (N,2) containing pixel box. AND'd with ra/dec
    stokes : int or list
        stokes dimension(s) to include in mask.  Default of -1 means all
    channels : int or list
        channel dimension(s) to include in mask.  Default of -1 means all

    Returns
    -------
    xarray Dataset
        New Dataset
    """
    import numpy as np
    import xarray as xr

    # type checking/conversion
    if not name.strip(): name = 'maskX'
    if ra is None: ra = [0.0, 0.0]
    if dec is None: dec = [0.0, 0.0]
    if pixels is None: pixels = np.zeros((1,2), dtype=int)-1
    pixels = np.array(pixels, dtype=int)
    if (pixels.ndim != 2) or (pixels.shape[1] != 2):
        print('ERROR: pixels parameter not a (N,2) array')
        return None
    stokes = np.array(np.atleast_1d(stokes), dtype=int)
    if stokes[0] == -1: stokes = [-1]
    channels = np.array(np.atleast_1d(channels), dtype=int)
    if channels[0] == -1: channels = [-1]

    # define mask within ra/dec range
    mask = xr.zeros_like(xds.image, dtype=bool).where((xds.right_ascension > np.min(ra)) &
                                                       (xds.right_ascension < np.max(ra)) &
                                                       (xds.declination > np.min(dec)) &
                                                       (xds.declination < np.max(dec)), True)

    # AND pixel values with ra/dec values
    mask = mask & xr.zeros_like(xds.image, dtype=bool).where((xds.d0 > np.min(pixels[:, 0])) &
                                                                (xds.d0 < np.max(pixels[:, 0])) &
                                                                (xds.d1 > np.min(pixels[:, 1])) &
                                                                (xds.d1 < np.max(pixels[:, 1])), True)

    # apply stokes and channels selections
    if stokes[0] >= 0:
      mask = mask & xr.zeros_like(xds.image, dtype=bool).where(xds.stokes.isin(xds.stokes[stokes]), True)
    if channels[0] >= 0:
      mask = mask & xr.zeros_like(xds.image, dtype=bool).where(xds.frequency.isin(xds.frequency[channels]), True)

    # assign region to a rest of image dataset
    xds = xds.assign(dict([(name, mask)]))

    return xds
