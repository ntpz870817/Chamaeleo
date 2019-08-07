"""
Name: Symmetrical testing for DDC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The Feasibility of Testing the Whole Process of DDC
"""

import Chamaeleo.codec_factory
import Chamaeleo.methods.yyc as yyc

read_file_path = "..\\..\\test\\test_files\\books\\A Tale of Two Cities.pdf"

write_file_path = "..\\..\\test\\generated_files\\target.pdf"

dna_path = "..\\..\\test\\generated_files\\target.dna"

model_path = "..\\..\\test\\generated_files\\yyc.pkl"

if __name__ == "__main__":
    tool = yyc.YYC()
    codec_factory.encode(method=tool, input_path=read_file_path, output_path=dna_path, model_path=model_path)
    del tool
    codec_factory.decode(model_path=model_path, input_path=dna_path, output_path=write_file_path)
