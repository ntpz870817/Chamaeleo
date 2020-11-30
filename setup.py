#!/usr/bin/env python

from setuptools import setup

setup(
    name="Chamaeleo",
    version="1.31",
    description="library for the well accepted coding schemes of DNA storage",
    long_description="Chamaeleo is currently the only collection focused on different codec methods for DNA storage. "
                     "This kit is mainly developed and operated by BGI-Research (Shenzhen). "
                     "It provides you a chance to use the classical coding schemes "
                     "to save files into DNA sequences or load them from DNA sequences.",
    author="Zhi PING, Hao-Ling ZHANG, Sha (Joe) ZHU",
    author_email="zhanghaoling@genomics.cn",
    url="https://github.com/ntpz870817/Chamaeleo",
    packages=[
        "Chamaeleo",
        "Chamaeleo.methods",
        "Chamaeleo.examples",
        "Chamaeleo.utils",
    ],
    package_data={
        "Chamaeleo": [
            "data/binaries/DNA Fountain Input Files.tar.gz",
            "data/binaries/Microsoft Winmine.exe",
            "data/books/A Tale of Two Cities.pdf",
            "data/books/The Wandering Earth.pdf",
            "data/musics/For Elise.wma",
            "data/musics/Summer.mp3",
            "data/pictures/Mona Lisa.jpg",
            "data/pictures/United Nations Flag.bmp",
            "data/videos/Exiting the Factory.flv",
            "data/videos/I have a Dream.mp4",
            "examples/log_files/robustness.logs",
            "examples/log_files/seq_features.logs",
        ]
    },
    package_dir={"Chamaeleo": "."},
    install_requires=[
        "reedsolo", "terminaltables"
    ],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="DNA Storage, Coding Scheme",
)
