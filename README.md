<p align="center">
<img src="./docs/source/_static/logo.png" alt="Chamaeleo" title="Chamaeleo" width="60%"/>
</p>

---

**Chamaeleo** is currently the only collection focused on different codec methods for DNA storage.
This kit is mainly developed and operated by Synthetic Platform of BGI-Research, for a detailed list of authors, see [**authors.md**](https://github.com/ntpz870817/Chamaeleo/blob/master/docs/source/authors.md).
It provides you a chance to use the classical DNA encoding and decoding methods to save files into DNA sequences or load them from DNA sequences.

---

Here, we provide guidance for different visitors.
We recommend that you read the user manual first and then the contributor manual.

- If you are a learner or a engineer, please pay attention to the user manual, see [**user_manual.md**](https://github.com/ntpz870817/Chamaeleo/blob/master/docs/source/user_manual.md).
- If you want to be a contributor, please pay attention to the contributor manual, see [**contributor_manual.md**](https://github.com/ntpz870817/Chamaeleo/blob/master/docs/source/contributor_manual.md).

---

**Chamaeleo** has undergone major adjustments before.
Versions smaller than **1.3** are unstable.
If you insist on using earlier versions, you may get unexpected results (especially actual information density).

You can find the latest version in:
(1) GitHub release [here](https://github.com/ntpz870817/Chamaeleo/releases/),
(2) PyPI website [here](https://pypi.org/project/Chamaeleo/).
Simply, installation through the command line (pip install Chamaeleo) is the easiest way to obtain the latest and most stable version of Chamaeleo.

As a kind suggestion, when you first touch this package, pipeline cases in the examples folder (please note [here](https://github.com/ntpz870817/Chamaeleo/tree/master/examples)) may help you get started well.

Sometimes the results (especially actual information density) obtained by Chamaeleo do not meet your expectations.
We recommend that you can check by following steps:
(1) related length settings include segment length, index length, and error-correction length.
(2) the method for calculating information density. For the built-in calculation method, it is bound inside the class AbstractCodingAlgorithm(please note [here](https://github.com/ntpz870817/Chamaeleo/blob/master/methods/default.py#L40)).

In some cases, you may encounter software errors. If you can't solve the problem, please describe your problem [here](https://github.com/ntpz870817/Chamaeleo/issues) or sent your problem to zhanghaoling@genomics.cn.

---

Here we declare the digital file used in our library for testing.

- DNA Fountain Input Files.tar:
http://files.teamerlich.org/dna_fountain/dna-fountain-input-files.tar.gz. Erlich, Y., & Zielinski, D. (2017). DNA Fountain enables a robust and efficient storage architecture. Science, 355(6328), 950-954.

- Microsoft Winmine.exe:
https://www.microsoft.com/en-us/p/microsoft-minesweeper/9wzdncrfhwcn?activetab=pivot:overviewtab. 2012 Microsoft Corporation.

- A Tale of Two Cities.pdf:
https://epdf.pub/a-tale-of-two-cities-penguin.html. Fictionwise.

- The Wandering Earth.pdf:
https://epdf.pub/the-wandering-earth.html. Beijing Guomi Digital Technology Co., Ltd.

- For Elise.wma:
https://www.youtube.com/watch?v=_mVW8tgGY_w.   Youtube.

- Summer.mp3:
https://www.youtube.com/watch?v=J7or0noYfMA. Youtube.

- Mona Lisa.jpg:
https://en.wikipedia.org/wiki/Mona_Lisa. wiki.

- United Nations Flag.bmp:
https://www.britannica.com/topic/flag-of-the-United-Nations

- Exiting the Factory.flv:
https://www.youtube.com/watch?v=DEQeIRLxaM4. Youtube.

- I have a Dream.mp4:
https://www.youtube.com/watch?v=MgYzJGmBXU8. Youtube.

---

If you think this repo helps or being used in your research, please consider refer this paper. 

[Chamaeleo: an integrated evaluation platform for DNA storage](http://www.synbioj.com/EN/abstract/abstract139.shtml)

with its [English version](https://www.biorxiv.org/content/10.1101/2020.01.02.892588v3)

Thank you!

English version:
````
@article{ping2020chamaeleo,
  title={Chamaeleo: an integrated evaluation platform for DNA storage},
  author={Ping, Zhi and Zhang, Haoling and Chen, Shihong and Zhuang, Qianlong and Zhu, Sha and Shen, Yue},
  journal={Synthetic Biology Journal},
  year={2020},
  pages={1-15},
}
````


Chinese version:
````
@article{ping2020chamaeleo,
  title={Chamaeleo:DNA存储碱基编解码算法的可拓展集成与系统评估平台},
  author={平质, 张颢龄, 陈世宏, 倪鸣, 徐讯, 朱砂, 沈玥},
  journal={合成生物学},
  year={2020},
  pages={1-15},
}
````
