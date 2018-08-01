from setuptools import setup

setup(
    name='aws-health-check',
    version='1.0',
    author="Mohammad Aftab Ali",
    author_email="maftabali@yahoo.com",
    description="Command line tool to check EC2 instances, volumes, snapshots and security groups",
    license="GPLv3+",
    packages=['awschecks'],
    url="https://github.com/maftabali/aws-health-check",
    install_requires=[
    'click',
    'boto3'
    ],
    entry_points='''
        [console_scripts]
        awschecks=awschecks.awschecks:cli
    ''',
)
