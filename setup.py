from setuptools import setup, find_packages

setup(
      name='ucimlrepo',
      version='0.0.6',
      description='A Python interface to import datasets from the UCI Machine Learning Repository',
      url='https://github.com/uci-ml-repo/ucimlrepo',
      author='Philip Truong',
      author_email='ucirepository@gmail.com',
      package_dir={'': 'src'},
      packages=find_packages(where='src')
)
