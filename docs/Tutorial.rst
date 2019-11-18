.. _sec-Tutorial:

Tutorial
========

Basic transcoding requirement
*****************************

The basic transcoding requirement is using the transcoding process once. In addition, users can also consider using the error-correction module once and also adding row indices before each bit segment once. In this situation, it is feasible to use codec_factory.py (in Chamaeleo/) directly.
This statement can by executed by Python programming tools or command line. Considering the many parameters in this statement, we recommend using the templates to accomplish these required tasks. Taking Yin-Yang code as an Example, the specific usage is as followed:

Using Python programming tools:

::

  # encode part
  from chamaeleo import *
  method = yyc.YYC()
  codec_factory.encode(method, input_path="C:/init.mp4", output_path="C:/target.dna", model_path="C:/yyc.pkl")
  # decode part
  codec_factory.decode(method, input_path="C:/target.dna", output_path="C:/target.mp4")
  # codec_factory.decode(input_path="C:/target.dna", output_path="C:/target.mp4", model_path="C:/yyc.pkl")

Using command line:

::

  # encode part
  $ codec_factory.encode(yyc.YYC(), input_path="C:/init.mp4", output_path="C:/target.dna", model_path="C:/yyc.pkl")
  # decode part
  $ codec_factory.decode(yyc.YYC(), input_path="C:/target.dna", output_path="C:/target.mp4")
  $ codec_factory.decode(input_path="C:/target.dna", output_path="C:/target.mp4", model_path="C:/yyc.pkl") $

In the two statements in codec_factory.py, the hyper parameters of encoding and encoding must correspond one by one. In the encoding process, codec_factory.encode(…), the hyper parameters are: method, input_path, output_path, model_path, verify, need_index, and segment_length. The decoding process, codec_factory.decode(…), is consistent with the hyper parameters of the encoding process. If need_index is True in encoding process, has_index needs True in decoding process. If verify is an instantiated method (=code) in the encoding process, verify=code needs in decoding process.


Transcoding requirements with highly customized
***********************************************

When we need highly customized coding and decoding programs for DNA storage, the basic
functions of codec_factory.py can provide will not be able to meet. We recommend using the
Python programming tools to accomplish these required tasks.

Transcoding method customization
--------------------------------

In the transcoding module, four transcoding method is collected. Here, we will discuss the hyper
parameters of these above four methods respectively.
Simple Code (see sc.py, in Chamaeleo/methods) has only one hyper parameter:
mapping_rule, which describes the mapping between bases and numbers.


Error-correction method customization
-------------------------------------
