#/usr/bin/env python3


import os
from setuptools import setup


def find_data(path):
    dir_content = []
    tree = [ (dirname, filenames) for dirname, _, filenames in os.walk(path)
             if filenames ]

    for root, files in tree:
        dir_content.extend(map(lambda x: os.path.join(root, x), files))

    return dir_content


def package_data():
    all_files = []
    for folder in ["Images", "Data"]:
        all_files.extend(find_data(folder))

    return all_files


setup(
    name = "pokemon-terminal",
    version = "0.0.1",

    description = "Pokemon terminal themes.",
    long_description = "",
    url = "https://github.com/LazoCoder/Pokemon-Terminal",

    author = "LazoCoder",
    author_email = "",

    license = "GPLv3",

    packages = [
        ".",
        "adapter",
        "adapter.implementations",
    ],

    package_data = {
        "": package_data(),
    },

    entry_points = {
        "console_scripts": [
            "pokemon = main:main",
            "ichooseyou = main:main",
        ],
    },

    keywords = "pokemon terminal theme style pokemon-terminal",

    classifiers = [
        "Development Status :: 3 - Alpha",

        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Topic :: Utilities",

        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    python_requires = ">=3.5"
)
