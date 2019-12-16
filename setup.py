from os.path import join, dirname
from setuptools import setup, find_packages



excludes = (
    '*test*',
    '*local_settings*',
) # yapf: disable

setup(name='py-mancala',
      version='1.0',
      license='syr',
      description='Mancala-Ai',
      author='Krzysztof Dorosz', "Hang Zhao", "Guoxing Yao"
      author_email='cypreess@gmail.com', 'hzhao18@syr.edu', 'gyao02@syr.edu'
      url='https://github.com/zhaohang930910/Mancala-Ai',
      platforms=['Any'],
      packages=find_packages(exclude=excludes),
      install_requires=[pytorch])
