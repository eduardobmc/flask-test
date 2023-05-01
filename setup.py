from setuptools import setup, find_packages


setup(
  name='mymodule',
  use_scm_version=True,
  setup_requires=[
    'wheel',
    'setuptools_scm',
  ],
  packages=find_packages(exclude=['tests']),
  install_requires=[
    'flask==2.3.2',
    'six==1.10.0',
  ],
)
