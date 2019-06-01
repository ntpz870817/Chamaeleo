"""
Name: Entry function

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): After initializing the encoding or decoding method,
             the conversion between DNA motif set and binary files is completed by the entry function.
"""


import sys
import utils.model_saver as saver
import utils.data_handle as data_handle
import utils.log as log


# noinspection PyProtectedMember
def encode(method, input_path, output_path, model_path=None):
    """
    introduction: Use the selected method, convert the binary file to DNA motif set and output it.

    :param method: Method under folder "methods/".
                    Type: Object.

    :param input_path: The path of binary file you need to convert.
                        Type: String.

    :param output_path: The path of DNA motif set you need to use to .
                         Type: String.

    :param model_path: The path of model file if you want to save
                        Type: String
    """

    if input_path is None or len(input_path) == 0:
        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                   "We did not obtain the path of file you need to encode!")

    if output_path is None or len(input_path) == 0:
        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                   "We did not obtain the path of generated file!")

    if model_path is not None:
        saver.save_model(model_path, method)

    input_matrix, size = data_handle.read_binary_from_all(input_path)

    dna_motifs = method.encode(input_matrix, size)

    data_handle.write_dna_file(output_path, dna_motifs)


# noinspection PyProtectedMember
def decode(method=None, model_path=None, input_path=None, output_path=None):
    """
    introduction:

    :param method: Method under folder "methods/".
                    If you have model file, you can use this function with out method.
                    Type: Object.

    :param input_path: The path of DNA motif set you need to convert.
                        Type: String.

    :param output_path: The path of binary file consistent with previous documents.
                         Type: String.

    :param model_path: The path of model file if you want to save
                        Type: String
    """

    if method is None and model_path is None:
        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                   "We did not obtain the method!")
    else:
        if input_path is None or len(input_path) == 0:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "We did not obtain the path of file you need to decode!")

        if output_path is None or len(input_path) == 0:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "We did not obtain the path of generated file!")

        if model_path is not None:
            method = saver.load_model(model_path)

        dna_motifs = data_handle.read_dna_file(input_path)

        output_matrix = method.decode(dna_motifs)

        data_handle.write_all_from_binary(output_path, output_matrix, method.file_size)
