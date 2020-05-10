from setuptools import setup

entry_points = {
    'console_scripts': [
        'whatportis=whatportis.cli:run',
    ]
}
readme = open('README.rst').read()

setup(
    name="whatportis",
    version="0.8.1",
    url='http://github.com/ncrocfer/whatportis',
    author='Nicolas Crocfer',
    author_email='ncrocfer@gmail.com',
    description="A command to search port names and numbers",
    long_description=readme,
    packages=['whatportis'],
    include_package_data=True,
    install_requires=[
        "simplejson==3.17.0",
        "tinydb==3.15.1",
        "requests==2.23.0",
        "prettytable==0.7.2",
        "click==7.1.2"
    ],
    extras_require={
        "dev": [
            "pytest",
            "tox"
        ],
        "server": [
            "flask==1.1.2"
        ]
    },
    entry_points=entry_points,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ),
)
