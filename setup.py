from setuptools import setup

entry_points = {
    'console_scripts': [
        'whatportis=whatportis.cli:run',
    ]
}
readme = open('README.rst').read()

setup(
    name="whatportis",
    version="0.8.2",
    url='http://github.com/ncrocfer/whatportis',
    author='Nicolas Crocfer',
    author_email='ncrocfer@gmail.com',
    description="A command to search port names and numbers",
    long_description=readme,
    packages=['whatportis'],
    include_package_data=True,
    install_requires=[
        "simplejson==3.17.2",
        "tinydb==4.4.0",
        "requests==2.25.1",
        "prettytable==2.1.0",
        "click==8.0.1"
    ],
    extras_require={
        "dev": [
            "pytest",
            "tox",
            "black"
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ),
)
