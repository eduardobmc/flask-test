from setuptools import setup, find_packages

setup(
  name='mymodule',
  version='1.0',
  packages=find_packages(exclude=['tests']),
  install_requires=[
    'flask==0.11',
    'six'
  ],
)
