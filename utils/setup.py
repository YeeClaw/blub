from setuptools import setup, find_packages

setup(
    name='blubBot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'discord.py',
        'mcstatus',
    ],
    entry_points={
        'console_scripts': [
            'blubBot = blubBot.__main__:main'
        ]
    }
)