
from setuptools import setup, find_packages
from systematic_networks import __version__

setup(
    name='systematic-networks',
    keywords='network subnet lookup utilities',
    description='python tools to look up information about networks',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    url='https://git.tuohela.net/systematic-components/systematic-networks',
    version=__version__,
    license='PSF',
    packages=find_packages(),
    python_requires='>3.6.0',
    entry_points={
        'console_scripts': [
            'netlookup=systematic_networks.bin.netlookup:main',
        ],
    },
    install_requires=(
        'dnspython>=1.16.0',
        'inflection>=0.4.0',
        'netaddr>=0.7.19',
        'requests>=2.23.0',
        'systematic-cli>=1.1.0',
    ),
    setup_requires=['tox'],
    tests_require=(),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'Topic :: System :: Systems Administration',
    ],
)
