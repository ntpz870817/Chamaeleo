"""
Name: Huffman Codec (DNA Storage Code based on Huffman code)

Reference: Goldman N, Bertone P, Chen S, et al. Towards practical, high-capacity, low-maintenance information storage in synthesized DNA[J]. Nature, 2013, 494(7435): 77.

Coder: HaoLing ZHANG (BGI-Research)[V1], QianLong ZHUANG (BGI-Research)

Current Version: 1

Function(s): (1) DNA encoding by Huffman Codec.
             (2) DNA decoding by Huffman Codec.
"""
import sys
import re

import Chamaeleo.utils.monitor as monitor
import Chamaeleo.utils.log as log
import Chamaeleo.methods.components.inherent as inherent


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyTypeChecker,PyUnusedLocal
class HC:
    def __init__(self, fixed_huffman=True, need_log=False):
        """
        introduction: The initialization method of Huffman Codec.

        :param fixed_huffman: Declare whether to use the Huffman dictionary in Goldman's paper.
                               In order to reduce the possible loss of function storage, we recommend using this dictionary.
        """

        log.output(
            log.NORMAL,
            str(__name__),
            str(sys._getframe().f_code.co_name),
            "Create the Huffman Codec method.",
        )

        self.huffman_tree = None
        self.segment_length = 0
        self.fixed_huffman = fixed_huffman
        self.file_size = 0
        self.m = monitor.Monitor()
        self.need_log = need_log

    # ================================================= encode part ========================================================

    def encode(self, matrix, size):
        """
        introduction: Encode DNA motifs from the data of binary file.

        :param matrix: Generated binary two-dimensional matrix.
                        The data of this matrix contains only 0 or 1 (non-char).
                        Type: int or bit.

        :param size: This refers to file size, to reduce redundant bits when transferring DNA to binary files.
                      Type: int

        :return dna_motifs: The DNA motif of len(matrix) rows.
                             Type: list(list(char)).
        """
        self.file_size = size

        self.segment_length = len(matrix[0])

        if self.segment_length % 8 != 0:
            temp_matrix = []
            for row in range(len(matrix)):
                temp_matrix.append([0 for col in range(self.segment_length % 8)] + matrix[row])
            matrix = temp_matrix

        self.m.restore()
        if self.need_log:
            log.output(
                log.NORMAL,
                str(__name__),
                str(sys._getframe().f_code.co_name),
                "Generate the huffman dictionary.",
            )
        if self.fixed_huffman:
            self.__huffman_dict__()
        else:
            self.__huffman_dict__(matrix)

        self.m.restore()
        if self.need_log:
            log.output(
                log.NORMAL,
                str(__name__),
                str(sys._getframe().f_code.co_name),
                "Convert matrix to dna motif set.",
            )
        dna_motifs = []

        for row in range(len(matrix)):
            if self.need_log:
                self.m.output(row, len(matrix))
            dna_motifs.append(
                self.__list_to_motif__(self.__huffman_compressed__(matrix[row]))
            )

        self.m.restore()
        return dna_motifs

    def __huffman_dict__(self, matrix=None):
        """
        introduction: Get the dictionary of Huffman tree.

        :param matrix: Generated binary two-dimensional matrix.
                        The data of this matrix contains only 0 or 1 (non-char).
                        Type: int or bit.
        """
        if matrix is None:
            self.huffman_tree = inherent.goldman_dict
        else:
            self.huffman_tree = self.__get_map__(matrix, 3)

    def __huffman_compressed__(self, binary_list):
        """
        introduction: Convert binary to ternary, compressing and facilitating the use of rotate code

        :param binary_list: One binary list.
                             Type: int or bit.

        :return ternary_list: One int list.
                               Type: List(int).
        """
        ternary_list = []

        for list_index in range(0, len(binary_list), 8):
            current_number = int(
                "".join(list(map(str, binary_list[list_index : list_index + 8]))), 2
            )
            huffman_code = self.huffman_tree[current_number]
            for code_index in range(len(huffman_code)):
                ternary_list.append(int(huffman_code[code_index]))

        return ternary_list

    def __list_to_motif__(self, one_list):
        """
        introduction: Encode a DNA motif from one binary list.

        :param one_list: One binary list.
                         Type: int or bit.

        :return dna_motif: One DNA motif.
                           Type: List(char).
        """
        last_base, dna_motif = "A", []
        for col in range(len(one_list)):
            current_base = inherent.rotate_codes.get(last_base)[one_list[col]]
            dna_motif.append(current_base)
            last_base = current_base

        return dna_motif

    def __get_map__(self, bit_matrix, size=None, multiple=3):
        """
        introduction: Customize Huffman tree based on the bit matrix.

        :param bit_matrix: Bit matrix, containing only 0,1.
                            Type: Two-dimensional list(int)

        :param size: File size corresponding to the matrix.

        :param multiple: Number of branches constructed (decimal semi-octets).

        :return tree: Byte-based (256) Huffman tree.
        """

        if size is None:
            size = len(bit_matrix) * len(bit_matrix[0])

        # Replace the bit matrix with one-dimensional decimal byte list
        decimal_list = self.__get_decimal_list__(bit_matrix, size)

        # Store elements and their weights, their codes
        weight, code = {}, {}
        # Recorder, prepare for the following screening of valid keys
        _node = lambda i: "_" + str(i).zfill(3)
        for one_byte in decimal_list:
            # Create weight values for each element
            if _node(one_byte) in weight:
                weight[_node(one_byte)] += 1
            else:
                # Set the initial value of the code
                code[_node(one_byte)] = ""
                weight[_node(one_byte)] = 1

        for one_byte in range(1, multiple - 1):
            # Add impossible elements to ensure normal combination and close as one element
            if (len(weight) - 1) % (multiple - 1) == 0:
                break
            else:
                weight["_" * one_byte] = 0
        weight_list = list(weight.items())

        for index in range(0, (len(weight) - 1) // (multiple - 1)):
            weight_list = sorted(weight_list, key=lambda x: x[0])
            weight_list = sorted(weight_list, key=lambda x: x[1])
            # Combine the previous terms into one term
            item = str(index).zfill(3)
            weight = 0
            # Add Huffman coding and form new combinations
            for branch in range(0, multiple):
                item += weight_list[branch][0]
                weight += weight_list[branch][1]
                # Add headers to each item of the previous items.
                for index_item in re.findall(r"_\d{3}", weight_list[branch][0]):
                    code[index_item] = str(multiple - branch - 1) + code[index_item]
            new = [(item, weight)]
            weight_list = weight_list[multiple:] + new

        dictionary = dict([int(key[1:]), value] for key, value in code.items())

        tree = []
        for index in range(256):
            tree.append(dictionary.get(index))

        return tree

    def __get_decimal_list__(self, bit_matrix, size):
        """
        introduction: Decimal list generated by the bit matrix.

        :param bit_matrix: Bit matrix, containing only 0,1.
                            Type: Two-dimensional list(int)

        :param size: File size corresponding to the matrix.

        :return decimal_list: Decimal list.
                              Type: One-dimensional list(int)
        """
        bit_index, temp_byte, decimal_list = 0, 0, []
        for row in range(len(bit_matrix)):
            for col in range(len(bit_matrix[0])):
                bit_index += 1
                temp_byte *= 2
                temp_byte += bit_matrix[row][col]
                if bit_index == 8:
                    if size >= 0:
                        decimal_list.append(int(temp_byte))
                        size -= 1
                    bit_index, temp_byte = 0, 0

        return decimal_list

    # ================================================= decode part ========================================================

    def decode(self, dna_motifs):
        """
        introduction: Decode DNA motifs to the data of binary file.

        :param dna_motifs: The DNA motif of len(matrix) rows.
                            Type: One-dimensional list(string).

        :return matrix: The binary matrix corresponding to the dna motifs.
                         Type: Two-dimensional list(int).

        :return file_size: This refers to file size, to reduce redundant bits when transferring DNA to binary files.
                            Type: int
        """

        self.m.restore()
        if self.need_log:
            log.output(
                log.NORMAL,
                str(__name__),
                str(sys._getframe().f_code.co_name),
                "Convert DNA motifs to binary matrix.",
            )

        matrix = []
        index_binary_length = int(len(str(bin(len(dna_motifs)))) - 2)

        for index in range(len(dna_motifs)):
            if self.need_log:
                self.m.output(index, len(dna_motifs))
            matrix.append(
                self.__huffman_decompressed__(
                    self.__motif_to_list__(dna_motifs[index]), index_binary_length
                )
            )

        if len(matrix[0]) != self.segment_length:
            temp_matrix = []
            for row in range(len(matrix)):
                temp_matrix.append(matrix[row][self.segment_length % 8:])
            matrix = temp_matrix

        self.m.restore()

        return matrix, self.file_size

    def __motif_to_list__(self, dna_motif):
        """
        introduction: Convert one DNA motif to one binary list.

        :param dna_motif: One DNA motif.
                           Type: List(char).

        :return one_list: One ternary Huffman coding list.
                           Type: List(int)
        """
        last_base, one_list = "A", []
        for index in range(len(dna_motif)):
            one_list.append(
                inherent.rotate_codes.get(last_base).index(dna_motif[index])
            )
            last_base = dna_motif[index]

        return one_list

    def __huffman_decompressed__(self, ternary_list, index_binary_length):
        """
        introduction: Conversion of ternary Huffman coding to binary coding.

        :param ternary_list: The ternary Huffman coding.

        :return binary_list: The binary list.
                              Type: list(int).
        """
        temp_ternary, binary_list = "", []
        for index in range(len(ternary_list)):
            temp_ternary += str(ternary_list[index])

            for tree_index in range(len(self.huffman_tree)):
                if temp_ternary == self.huffman_tree[tree_index]:
                    if len(binary_list) + 8 < self.segment_length + index_binary_length:
                        binary_list += list(
                            map(int, list(str(bin(tree_index))[2:].zfill(8)))
                        )
                    else:
                        remaining_length = (
                            self.segment_length + index_binary_length - len(binary_list)
                        )
                        binary_list += list(
                            map(
                                int,
                                list(str(bin(tree_index))[2:].zfill(remaining_length)),
                            )
                        )
                    temp_ternary = ""
                    break

        return binary_list
