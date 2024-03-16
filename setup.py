from pathlib import Path
from setuptools import setup, find_packages

about = {}
here = Path.absolute(Path(__file__).parent)
with here.joinpath('src', '__init__.py').open(mode='r') as input_stream:
    exec(input_stream.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],

    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],

    packages=[
        "bbprograms",
        "core"
    ],
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "boto3",
        "pydantic"
    ],
    license=about['__license__'],
    description=about['__description__']
)
