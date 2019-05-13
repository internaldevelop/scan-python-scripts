#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# A very simple setup script to create a single executable
#
# hello.py is a very simple 'Hello, world' type script which also displays the
# environment in which the script runs
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

options={
	'build_exe':{
		'includes':['os','time','sys','subprocess','socket','json','usb','Crypto']

	}

}


executables = [
    Executable('mainFrame.py')
]

setup(name='SecurityCfgCheck',
      version='1.0',
      description='Securyty configuration check',
      executables=executables,
      options=options
      )