from setuptools import setup, find_packages


__title__ = 'asman'
__description__ = 'The package with core functionality for Asman'
__url__ = 'https://github.com/asman-go/core'
__version__ = '0.0.1'
__author__ = 'Petrakov Oleg'
__author_email__ = 'murami.ike@gmail.com'
__license__ = 'MIT'

setup(
    name=__title__,
    version=__version__,

    url=__url__,
    author=__author__,
    author_email=__author_email__,

    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        'boto3',
        'pydantic',
        'pydantic_settings',
        'grpcio',
        'grpcio-tools',
        'setuptools',
        'mock',
        'moto[all]',
        'pytest'
    ],
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage']
    # },
    license=__license__,
    description=__description__
)
