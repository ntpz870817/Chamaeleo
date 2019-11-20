#!/usr/bin/env python

from setuptools import setup

setup(
    name="Chamaeleo",
    version="0.1",
    description="library for the well accepted coding schemes of DNA storage",
    long_description="Chamaeleo is currently the only collection focused on different codec methods for DNA storage. This kit is mainly developed and operated by BGI-Research (Shenzhen). It provides you a chance to use the classical DNA encoding and decoding methods to save files into DNA motifs or load them from DNA motifs.",
    author="Zhi PING, Hao-Ling ZHANG, Sha (Joe) ZHU",
    author_email="zhanghaoling@genomics.cn",
    url="https://github.com/ntpz870817/Chamaeleo",
    packages=["Chamaeleo",
              "Chamaeleo.methods",
              "Chamaeleo.methods.components",
              "Chamaeleo.methods.verifies",
              "Chamaeleo.utils"],
    package_dir={"Chamaeleo": "."},
    license='MIT',
    keywords='DNA Storage, Coding Scheme'
)
