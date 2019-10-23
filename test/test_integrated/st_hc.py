"""
Name: Symmetrical testing for HC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The Feasibility of Testing the Whole Process of HC
"""

import sys
import os

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

import codec_factory
import methods.hc as hc

read_file_path = "..\\..\\test\\test_files\\books\\A Tale of Two Cities.pdf"

write_file_path = "..\\..\\test\\generated_files\\target.pdf"

dna_path = "..\\..\\test\\generated_files\\target.dna"

model_path = "..\\..\\test\\generated_files\\hc.pkl"

if __name__ == "__main__":
    tool = hc.HC()
    codec_factory.encode(method=tool, input_path=read_file_path, output_path=dna_path, model_path=model_path, need_index=False)
    del tool
    codec_factory.decode(model_path=model_path, input_path=dna_path, output_path=write_file_path, has_index=False)
