from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='serverMonitoring',
    version='0.5.0',
    description='Monitoring script for servers using SystemD',
    long_description="A monitoring tool checking server status via SystemD and some vital constants (CPU, Disk Usage, "
                     "Load average and RAM utilization) and sending alerts through notification channels",
    url='https://github.com/mysocialbook/serverMonitoring',
    author='The MySocialBook team',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License ::AGPL v3 License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],
    keywords='monitoring linux systemd slack development',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['slackclient', 'boto3', 'psutil', 'pyCLI'],
    package_data={  # Optional
        'sample': ['config.ini'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={
        'console_scripts': [
            'monitor=Monitoring:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/mysocialbook/serverMonitoring/issues',
        'Source': 'https://github.com/mysocialbook/serverMonitoring',
    },
)
