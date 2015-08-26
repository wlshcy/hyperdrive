#!/usr/bin/env python

from setuptools import setup

setup(name='hyperdrive',
      version='1.0',
      description='api driver',
      author='nmg',
      author_email='nmg1986@126.com',
      url='https://github.com/nmg1986/hyperdrive.git',

      packages=['hyperdrive',
		'hyperdrive.common',
		'hyperdrive.api',
		'hyperdrive.db',
	       ],

      scripts=['bin/hyperdrive'],

      data_files=[('/etc/hyperdrive',['etc/hyperdrive.conf',
			       'etc/api-paste.ini',
			      ]
		 )]
)
