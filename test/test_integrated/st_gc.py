"""
Name: Symmetrical testing for CC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The Feasibility of Testing the Whole Process of GC
"""

import sys
import os

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

import codec_factory
import methods.gc as cc


read_file_path = "..\\..\\test\\test_files\\books\\A Tale of Two Cities.pdf"

write_file_path = "..\\..\\test\\generated_files\\target.pdf"

dna_path = "..\\..\\test\\generated_files\\target.dna"

model_path = "..\\..\\test\\generated_files\\gc.pkl"


# noinspection PyProtectedMember
if __name__ == "__main__":
    tool = cc.GC([index for index in range(48)])
    codec_factory.encode(method=tool, input_path=read_file_path, output_path=dna_path, model_path=model_path)
    del tool
    codec_factory.decode(model_path=model_path, input_path=dna_path, output_path=write_file_path)
