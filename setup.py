from setuptools import setup
import os

version_str = os.getenv('RELEASE_VERSION')

setup(
    name='fff-mock-gen',
    version=version_str,
    author="Alex Pabouctsidis",
    author_email='alex.pabouct@gmail.com',
    url='https://github.com/Amcolex/fff-mock-gen.git',
    description = "Automatic mock generation using FFF",
    long_description="Scan a C header file and generate a mock file using FFF",
    py_modules=['fff_mock_gen'],
    packages=['fff_mock_gen'],
    include_package_data=True,

    entry_points='''
        [console_scripts]
        fff-mock-gen=fff_mock_gen.fff_mock_gen:main
    ''',
)