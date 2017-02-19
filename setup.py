from setuptools import setup, find_packages


setup(
  name='mymodule',
  use_scm_version=True,
  setup_requires=[
    'setuptools_scm',
  ],
  packages=find_packages(exclude=['tests']),
  install_requires=[
    'flask==0.12',
    'six==1.10.0',
  ],
)
