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


def region(xds, name='region1', ra=None, dec=None, pixels=None, stokes=-1, channels=-1):
    """
    Create a new region Data variable in the Dataset \n
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
        array of shape (N,2) containing pixel box. OR'd with ra/dec
    stokes : int or list
        stokes dimension(s) to include in region.  Default of -1 means all
    channels : int or list
        channel dimension(s) to include in region.  Default of -1 means all
        
    Returns
    -------
    xarray Dataset
        New Dataset
    """
    import numpy as np
    import dask.array as da
    import xarray as xr
    
    # type checking/conversion
    if not name.strip(): name = 'regionX'
    if ra is None: ra=[0.0, 0.0]
    if dec is None: dec=[0.0, 0.0]
    if pixels is None: pixels = np.zeros((1,2), dtype=int)-1
    pixels = np.array(pixels, dtype=int)
    if (pixels.ndim != 2) or (pixels.shape[1] != 2):
      print('ERROR: pixels parameter not a (N,2) array')
      return None
    stokes = np.array(np.atleast_1d(stokes), dtype=int)
    if stokes[0] == -1: stokes = list(range(len(xds['stokes'])))
    channels = np.array(np.atleast_1d(channels), dtype=int)
    if channels[0] == -1: channels = list(range(len(xds['frequency'])))
    
    # TBD: allow arbitrary pixels, not just rectangles
    #ind_x = xr.DataArray(list(pixels[:,0]), dims=['d0'])
    #ind_y = xr.DataArray(list(pixels[:,1]), dims=['d1'])
    #region = xds.image[ind_x, ind_y]
    
    # TESTING only
    # ra = [2.88788, 2.88793]
    # dec = [-0.60573, -0.60568]
    # pixels = np.array([[20,40],[80,500]])
    
    # define region within ra/dec range
    region = xr.ones_like(xds.image,dtype=bool).where((xds.right_ascension > np.min(ra)) & 
                                                      (xds.right_ascension < np.max(ra)) &
                                                      (xds.declination > np.min(dec)) & 
                                                      (xds.declination < np.max(dec)), False)
    
    # OR pixel values with ra/dec values
    #region = region | xr.ones_like(xds.image,dtype=bool).where(xds.d0.isin(pixels[:,0]) &
    #                                                           xds.d1.isin(pixels[:,1]), False)
    region = region | xr.ones_like(xds.image,dtype=bool).where((xds.d0 > np.min(pixels[:,0])) &
                                                               (xds.d0 < np.max(pixels[:,0])) &
                                                               (xds.d1 > np.min(pixels[:,1])) &
                                                               (xds.d1 < np.max(pixels[:,1])), False)
    
    # apply stokes and channels selections
    region = region.where(xds.stokes.isin(xds.stokes[stokes]), False)
    region = region.where(xds.frequency.isin(xds.frequency[channels]), False)
    
    # assign region to a rest of image dataset
    xds = xds.assign(dict([(name,region)]))
    return xds
    
