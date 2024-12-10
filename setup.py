from setuptools import setup, find_packages

from atvm import __version__

setup(
  name='atvm',
  version=__version__,
  url='http://github.com/riwahachem/Projet_HAX712X',
  description="ATVM - Analyse du Trafic VéloMagg de Montpellier",
  author='riwahachem',
  author_email='riwahachemreda@gmail.com',
  license='MIT',
  packages=find_packages()
)