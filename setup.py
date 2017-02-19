from setuptools import setup
from shell import shell

setup(
    name='DAQ-CLI',
    version=shell.Shell.version,
    py_modules=['shell'],
    install_requires=[
        'PyDAQmx',
        'numpy',
    ],
    entry_points='''
        [shell:shell.py]

    ''',
)