from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as fid:
    long_description = fid.read()

setup(
    name='cngi_prototype',
    version='0.0.24',
    description='CASA Next Generation Infrastructure Prototype',
    long_description=long_description,
    author='National Radio Astronomy Observatory',
    author_email='casa-feedback@nrao.edu',
    url='https://github.com/casangi/cngi_prototype',
    license='Apache-2.0',
    packages=find_packages(),
    install_requires=['numpy==1.17.3',
                      'numba==0.47.0',
                      'dask==2.9.0',
                      'bokeh==1.3.4',
                      'pandas==0.25.2',
                      'xarray==0.14.1',
                      'zarr==2.3.2',
                      'numcodecs==0.6.4',
                      'matplotlib==3.1.2',
                      'sparse==0.8.0'],
)
