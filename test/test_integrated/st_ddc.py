"""
Name: Symmetrical testing for DDC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The Feasibility of Testing the Whole Process of DDC
"""

import Chamaeleo.methods.ddc as ddc
import Chamaeleo.methods.components.index_operator as index_operator

import Chamaeleo.utils.model_saver as saver
import Chamaeleo.utils.data_handle as data_handle

read_file_path = "..\\..\\test\\test_files\\books\\A Tale of Two Cities.pdf"
write_file_path = "..\\..\\test\\generated_files\\target.pdf"

dna_path = "..\\..\\test\\generated_files\\target.dna"

model_path = "..\\..\\test\\generated_files\\ddc.pkl"

if __name__ == "__main__":
    input_matrix, size = data_handle.read_binary_from_all(read_file_path)
    input_matrix = index_operator.connect_all(input_matrix)
    tool = ddc.DDC()
    dna_motifs = tool.encode(input_matrix, size)

    data_handle.write_dna_file(dna_path, dna_motifs)
    saver.save_model(model_path, tool)

    tool = saver.load_model(model_path)
    dna_motifs = data_handle.read_dna_file(dna_path)
    output_matrix, size = tool.decode(dna_motifs)
    indexes, data_set = index_operator.divide_all(output_matrix)
    output_matrix = index_operator.sort_order(indexes, data_set)
    data_handle.write_all_from_binary(write_file_path, output_matrix, size)
