#!/usr/bin/env python

from distutils.core import setup

setup(
    name="Chamaeleo",
    version="0.0",
    description="library for the well accepted coding schemes of DNA storage",
    author="Zhi PING, Hao-Ling ZHANG, Sha (Joe) ZHU",
    author_email="",
    url="https://github.com/ntpz870817/Chamaeleo",
    packages=["Chamaeleo", "Chamaeleo.methods", "Chamaeleo.utils"],
    package_dir={"Chamaeleo": "."},
    package_data={
        "Chamaeleo": [
            "test/test_files/binaries/DNA Fountain Input Files.tar",
            "test/test_files/binaries/Microsoft Winmine.exe",
            "test/test_files/books/A Tale of Two Cities.pdf",
            "test/test_files/books/The Wandering Earth.pdf",
            "test/test_files/musics/For Elise (Ludwig van Beethoven).wma",
            "test/test_files/musics/Grande Sonata Pathetique OP.13.mp3",
            "test/test_files/pictures/Mona Lisa.jpg",
            "test/test_files/pictures/United Nations Flag.bmp",
            "test/test_files/videos/Exiting the Factory (the First Movie in the World).flv",
            "test/test_files/videos/I have a Dream (Martin Luther King).mp4",
        ]
    },
    install_requires=[
        'numpy>=1.17.0',
    ],

)
