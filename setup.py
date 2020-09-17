from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='transference',
    version='1.0',
    description='A useful module',
    long_description=long_description,
    author='Man Foo',
    author_email='foomail@foo.com',
    packages=['transference'],  # same as name
    install_requires=['tqdm'],  # external packages as dependencies
    scripts=[
        'receiver/receiver.py',
        'sender/sender.py',
    ]
)
