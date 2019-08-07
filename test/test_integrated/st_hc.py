"""
Name: Symmetrical testing for HC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The Feasibility of Testing the Whole Process of HC
"""


import Chamaeleo.methods.hc as hc

import Chamaeleo.codec_factory


read_file_path = "H:/A Tale of Two Cities.pdf"
write_file_path = "H:/target.pdf"

dna_path = "H:/target.dna"

model_path = "H:/hc.pkl"

if __name__ == "__main__":
    tool = hc.HC()
    codec_factory.encode(method=tool, input_path=read_file_path, output_path=dna_path, model_path=model_path)
    codec_factory.decode(model_path=model_path, input_path=dna_path, output_path=write_file_path)
