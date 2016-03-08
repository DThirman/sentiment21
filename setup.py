from setuptools import setup

setup(
    name='sentiment21',
    version='0.1',
    py_modules=['sentiment21'],
        install_requires=[
            'Click',
    ],
    entry_points='''
        [console_scripts]
        sentiment21=sentiment21:cli
    ''',
)
