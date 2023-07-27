from setuptools import setup, find_packages

setup(
      name='ucimlrepo',
      version='0.0.1',
      description='A Python interface to import datasets from the UCI Machine Learning Repository',
      url='https://github.com/uci-ml-repo/ucimlrepo',
      author='Philip Truong',
      author_email='philtr928@example.com',
      license='MIT',
      install_requires=[
          'pandas',
      ],
      packages=find_packages(exclude=("tests", "test.*", "*test*")),
)
