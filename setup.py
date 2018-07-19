#!/usr/bin/env python3
import os
from setuptools import setup, find_packages


def find_data(relpath, folder):
    dir_content = []
    path = os.path.join(relpath, folder)
    tree = [(dirname, filenames) for dirname, _, filenames in os.walk(path)
            if filenames]

    for root, files in tree:
        path = os.path.relpath(root, relpath)
        dir_content.extend(map(lambda x: os.path.join(path, x), files))

    return dir_content


def package_data(relpath, folders):
    all_files = []
    for folder in folders:
        all_files.extend(find_data(relpath, folder))

    return all_files


setup(
    name="pokemon-terminal",
    version="1.1.0",  # Copied from package.json

    description="Pokemon terminal themes.",
    long_description="""
Pokemon Terminal Themes.

719 unique Pokemon.
from Kanto, Johto, Hoenn, Sinnoh, Unova, and Kalos.

Change the Terminal Background & Desktop Wallpaper.
Supports iTerm2, Terminology, Tilix and ConEmu.""",
    url="https://github.com/LazoCoder/Pokemon-Terminal",

    author="LazoCoder",
    author_email="",

    license="GPLv3",

    packages=find_packages(exclude=['tests']),

    package_data={
        "pokemonterminal": package_data("pokemonterminal", ["Data", "Images"]),
    },

    entry_points = {
        'console_scripts': [
            'pokemon = pokemonterminal.main:main',
            'ichooseyou = pokemonterminal.main:main',
        ],
    },

    keywords="pokemon terminal theme style pokemon-terminal",

    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Topic :: Utilities",

        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    python_requires=">=3.6"
)
