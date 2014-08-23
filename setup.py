from setuptools import setup

setup(
    name='beetle_watcher',
    author='Jeppe Toustrup',
    author_email='jeppe@tenzer.dk',
    packages=[
        'beetle_watcher'
    ],
    install_requires=[
        'watchdog==0.8.1',
    ],
)
