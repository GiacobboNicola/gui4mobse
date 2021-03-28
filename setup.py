#!/usr/bin/env python

try:
  from setuptools import setup
  from setuptools.command.install import install
except ImportError:
  from distutils.core import setup
  from distutils.command.install import install

import subprocess


def load_mobse():
  from tools import download
  instance = download.GetMOBSE('mobse')
  instance.main()

def compile_mobse():
  subprocess.run(['make','clean'])
  subprocess.run(['make','mobseGUI'])

class InstallMOBSECommand(install):
  def run(self):
    install.run(self)
    load_mobse()
    #compile_mobse()

setup(
  name = 'GUI4MOBSE',
  version = '0.1',      
  license ='MIT',  
  description = 'Graphic Unit Interface for `MOBSE <https://mobse-webpage.netlify.app>`.',
  #long_description='See the github `repository <https://github.com/GiacobboNicola/PubRec>`_.',
  #long_description_content_type="text/markdown",
  author = 'Nicola Giacobbo',
  author_email = 'giacobbo.nicola@gmail.com', 
  url = 'https://github.com/GiacobboNicola/gui4mobse',   
  #download_url = 'https://github.com/GiacobboNicola/PubRec/archive/v1.0.1.tar.gz', 
  keywords = ['MOBSE', 'GUI', 'PySimpleGUI'],
  py_modules = ['gui4mobse'],
  scripts = ['bin/gui4mobse'],
  #packages=setuptools.find_packages(),
  install_requires = [ 
          'PySimpleGUI',
          'Pillow',
          'pybase64',
          'pandas'
      ],
  cmdclass = {
          'install': InstallMOBSECommand,
  },
  include_package_data = True,
  classifiers = [
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
