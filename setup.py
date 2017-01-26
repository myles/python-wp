from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests'
]

test_requirements = []

setup(
    name='python-wordpress',
    version='0.1.0',
    author='Myles Braithwaite',
    author_email='me@mylesbraithwaite.com',
    description='A Python Library for WordPress.',
    keywords='wordpress',
    url='https://github.com/myles/python-wordpress',
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
