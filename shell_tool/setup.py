from setuptools import setup

import  intrepreter
setup(
    name='intrepreter',
    version='0.1',
    py_modules=['intrepreter'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        intrepreter=intrepreter:cli
    ''',
)