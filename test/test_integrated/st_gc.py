"""
Name: Symmetrical testing for CC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The Feasibility of Testing the Whole Process of GC
"""
import sys

import methods.gc as cc

import utils.model_saver as saver
import utils.data_handle as data_handle
import utils.log as log


read_file_path = "..\\..\\test\\test_files\\books\\A Tale of Two Cities.pdf"
write_file_path = "..\\..\\test\\generated_files\\target.pdf"

dna_path = "..\\..\\test\\generated_files\\target.dna"

model_path = "..\\..\\test\\generated_files\\cc.pkl"

# noinspection PyProtectedMember
if __name__ == '__main__':
    tool = cc.GC([index for index in range(0, 48)])
    input_matrix, size = data_handle.read_binary_from_all(read_file_path, segment_length=160)
    dna_motifs = tool.encode(input_matrix, size)
    data_handle.write_dna_file(dna_path, dna_motifs)
    saver.save_model(model_path, tool)

    tool = saver.load_model(model_path)
    dna_motifs = data_handle.read_dna_file(dna_path)
    output_matrix, size = tool.decode(dna_motifs)
    data_handle.write_all_from_binary(write_file_path, output_matrix, size)
