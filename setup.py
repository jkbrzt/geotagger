import codecs

from setuptools import setup, find_packages

from geotagger import __version__


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()


def install_requires():
    with codecs.open('requirements.txt', encoding='utf8') as f:
        reqs = f.read()
    return reqs.strip().split()


setup(
    name='geotagger',
    version=__version__,
    description='Geotag photos with exiftool based on your Moves app history',
    long_description=long_description(),
    url='https://github.com/jakubroztocil/geotagger',
    download_url='https://github.com/jakubroztocil/geotagger',
    author='Jakub Roztocil',
    author_email='jakub@roztocil.co',
    license='MIT',
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'geotagger = geotagger.__main__:main',
        ],
    },
    install_requires=install_requires(),
    classifiers=[],
)
