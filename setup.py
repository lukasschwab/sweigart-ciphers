from setuptools import setup


setup(
    name="crypto",
    version="0.0.1",
    packages=['crypto'],

    # dependencies
    install_requires=[],
    entry_points={
        'console_scripts': [
            'crypto=crypto.crypto_core:main'
        ]
    }
)