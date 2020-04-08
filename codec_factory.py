"""
Name: Entry function

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): After initializing the encoding or decoding method,
             the conversion between DNA sequence set and binary files is completed
             by the entry function.
"""
import sys

import Chamaeleo.utils.model_saver as saver
import Chamaeleo.utils.data_handle as data_handle
import Chamaeleo.utils.log as log
import Chamaeleo.methods.components.index_operator as index_operator


# noinspection PyProtectedMember
def encode(method, input_path, output_path,
           model_path=None, verify=None, need_index=True, segment_length=120, need_log=False):
    """
    introduction: Use the selected method, convert the binary file to DNA sequence
                  set and output the DNA sequence set.

    :param method: Method under folder "methods/".
                    Type: Object.

    :param input_path: The path of binary file you need to convert.
                        Type: String.

    :param output_path: The path of DNA sequence set you need to use to .
                         Type: String.

    :param model_path: The path of model file if you want to save
                        Type: String

    :param verify: Error correction method under "methods/verifies/"
                    Type: Object.

    :param need_index: Declare whether the binary sequence indexes are required
                       in the DNA sequences.
                        Type: bool.

    :param segment_length: The cut length of DNA sequence.
                      Considering current DNA synthesis factors, we usually
                      set 120 bases as a sequence.

    :param need_log: Show the log.
    """

    if input_path is None or len(input_path) == 0:
        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                   "The input file path is invalid!")

    if output_path is None or len(input_path) == 0:
        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                   "The output file path is invalid!")

    input_matrix, size = data_handle.read_binary_from_all(input_path, segment_length, need_log)

    if need_index:
        input_matrix = index_operator.connect_all(input_matrix, need_log)

    if verify is not None:
        input_matrix = verify.add_for_matrix(input_matrix, need_log)

    dna_sequences = method.encode(input_matrix, size, need_log)

    if model_path is not None:
        saver.save_model(model_path, {"method": method, "verify": verify})

    data_handle.write_dna_file(output_path, dna_sequences, need_log)


# noinspection PyProtectedMember
def decode(method=None, model_path=None, input_path=None, output_path=None,
           verify=None, has_index=True, need_log=False):
    """
    introduction: Use the selected method, convert DNA sequence set to the binary
                  file and output the binary file.

    :param method: Method under folder "methods/".
                    If you have model file, you can use this function with out
                    method.
                    Type: Object.

    :param input_path: The path of DNA sequence set you need to convert.
                       Type: String.

    :param output_path: The path of binary file consistent with previous
                        documents.
                         Type: String.

    :param model_path: The path of model file if you want to save
                        Type: String

    :param verify: Error correction method under "methods/verifies/"
                    Type: Object.

    :param has_index: Declare whether the DNA sequences contain binary sequence
                      indexes.
                       Type: bool.

    :param need_log: Show the log.
    """

    if method is None and model_path is None:
        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                   "The method you select does not exist!")
    else:
        if input_path is None or len(input_path) == 0:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "The input file path is not valid!")

        if output_path is None or len(input_path) == 0:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "The output file path is not valid!")

        if model_path is not None:
            model = saver.load_model(model_path)
            method = model.get("method")
            verify = model.get("verify")

        dna_sequences = data_handle.read_dna_file(input_path, need_log)

        output_matrix, size = method.decode(dna_sequences, need_log)

        if verify is not None:
            output_matrix = verify.verify_for_matrix(output_matrix, need_log)

        if has_index:
            indexes, data_set = index_operator.divide_all(output_matrix, need_log)
            output_matrix = index_operator.sort_order(indexes, data_set, need_log)

        data_handle.write_all_from_binary(output_path, output_matrix, size, need_log)
