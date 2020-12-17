
from setuptools import setup, find_packages
from netlookup import __version__

setup(
    name='netlookup',
    keywords='network subnet lookup utilities',
    description='Python tools to look up information about networks',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    url='https://git.tuohela.net/python/netlookup',
    version=__version__,
    license='PSF',
    packages=find_packages(),
    python_requires='>3.6.0',
    entry_points={
        'console_scripts': [
            'netlookup=netlookup.bin.netlookup:main',
        ],
    },
    install_requires=(
        'cli-toolkit>=1.0.2',
        'dnspython>=1.16.0',
        'inflection>=0.4.0',
        'netaddr>=0.7.19',
        'requests>=2.23.0',
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
