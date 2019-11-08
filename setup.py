#!/usr/bin/env python

from setuptools import setup

setup(
    name="Chamaeleo",
    version="0.1",
    description="library for the well accepted coding schemes of DNA storage",
    author="Zhi PING, Hao-Ling ZHANG, Sha (Joe) ZHU",
    author_email="pingzhi@cngb.org, zhanghaoling@genomics.cn",
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
