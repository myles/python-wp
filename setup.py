from setuptools import setup

from wordpress._meta import __version__, __project_name__, __project_link__

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests'
]

test_requirements = []

setup(
    name=__project_name__,
    version=__version__,
    author='Myles Braithwaite',
    author_email='me@mylesbraithwaite.com',
    description='A Python Library for WordPress.',
    keywords='wordpress',
    url=__project_link__,
    packages=['wordpress'],
    package_dir={'wordpress': 'wordpress'},
    include_package_data=True,
    long_description=readme,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    license='MIT license',
    install_requires=requirements,
    zip_safe=False,
    test_suite='tests',
    tests_require=test_requirements
)
