"""
Name: Symmetrical testing for DDC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The Feasibility of Testing the Whole Process of DDC
"""
import sys

import methods.ddc as ddc
import methods.components.index_operator as index_operator

import utils.model_saver as saver
import utils.data_handle as data_handle
import utils.log as log


read_file_path = "..\\..\\test\\test_files\\founding ceremony.mp4"
write_file_path = "..\\..\\test\\generated_files\\target.mp4"

dna_path = "..\\..\\test\\generated_files\\target.dna"

model_path = "..\\..\\test\\generated_files\\ddc.pkl"

if __name__ == '__main__':
    tool = ddc.DDC()
    input_matrix = data_handle.read_binary_from_all(read_file_path)
    input_matrix = index_operator.connect_all(input_matrix)
    dna_motifs = tool.encode(input_matrix)
    data_handle.write_dna_file(dna_path, dna_motifs)
    saver.save_model(model_path, tool)

    tool = saver.load_model(model_path)
    dna_motifs = data_handle.read_dna_file(dna_path)
    output_matrix = tool.decode(dna_motifs)
    log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
               "Divide index and data from binary matrix.")
    indexs, datas = index_operator.divide_all(output_matrix)
    log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
               "Restore the disrupted data order.")
    output_matrix = index_operator.sort_order(indexs, datas)

    data_handle.write_all_from_binary(write_file_path, output_matrix)
