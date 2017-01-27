import sys
from setuptools import setup, find_packages, __version__

v = sys.version_info
if sys.version_info < (3, 5):
    msg = "FAIL: Requires Python 3.5 or later, " \
          "but setup.py was run using {}.{}.{}"
    v = sys.version_info
    print(msg.format(v.major, v.minor, v.micro))
    print("NOTE: Installation failed. Run setup.py using python3")
    sys.exit(1)


setup(
    name='sovrin-agent',
    version=__version__,
    description='Sovrin Agent',
    long_description='Reference implementation of a Sovrin Agent',
    url='https://github.com/evernym/sovrin-agent',
    author=__author__,
    author_email='dev@evernym.us',
    license=__license__,
    keywords='Sovrin agent identity plenum',
    packages=find_packages(exclude=['test', 'test.*', 'docs', 'docs*']) + ['data', ],
    package_data={
        '':       ['*.txt',  '*.md', '*.rst', '*.json', '*.conf', '*.html',
                   '*.css', '*.ico', '*.png', 'LICENSE', 'LEGAL']},
    include_package_data=True,
    install_requires=['sovrin'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    scripts=['scripts/startApiServer', 'scripts/startApiServerDebug']
)
