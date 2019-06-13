"""
Name: Huffman Codec (DNA Storage Code based on Huffman code)

Reference: Goldman N, Bertone P, Chen S, et al. Towards practical, high-capacity, low-maintenance information storage in synthesized DNA[J]. Nature, 2013, 494(7435): 77.

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) DNA encoding by Huffman Codec.
             (2) DNA decoding by Huffman Codec.
"""

import csv
import sys
import os
import utils.monitor as monitor
import utils.log as log
import methods.components.inherent as inherent
import methods.components.index_operator as index_data
import methods.components.huffman_creator as tree_creator


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyTypeChecker,PyUnusedLocal
class HC:
    def __init__(self, fixed_huffman=True):
        self.huffman_tree = None
        self.segment_length = 0
        self.fixed_huffman = fixed_huffman
        self.m = monitor.Monitor()

# ================================================= encode part ========================================================

    def encode(self, matrix):
        """
        introduction: Encode DNA motifs from the data of binary file.

        :param matrix: Generated binary two-dimensional matrix.
                        The data of this matrix contains only 0 or 1 (non-char).
                        Type: int or bit.

        :return dna_motifs: The DNA motif of len(matrix) rows.
                             Type: list(list(char)).
        """
        self.segment_length = len(matrix[0])

        self.m.restore()
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Generate the huffman dictionary.")
        if self.fixed_huffman:
            self.__huffman_dict__()
        else:
            self.__huffman_dict__(matrix)

        self.m.restore()
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Change matrix to dna motif set.")
        dna_motifs = self.__get_dna_motifs__(matrix)

        return dna_motifs

    def __huffman_dict__(self, matrix=None):
        """
        introduction: Get the dictionary of Huffman tree.

        :param matrix: Generated binary two-dimensional matrix.
                        The data of this matrix contains only 0 or 1 (non-char).
                        Type: int or bit.
        """
        if matrix is None:
            huff_dict = open(os.path.join(os.path.dirname(__file__), "components/huffman.dict"), "r")
            csv_reader = csv.reader(huff_dict, delimiter=',')
            tree = []
            for row in csv_reader:
                tree.append(row[1])
        else:
            tree = tree_creator.get_map(matrix, 3)

        self.huffman_tree = tree
        print(self.huffman_tree)

    def __get_dna_motifs__(self, matrix):
        """
        introduction: Get dna motif set from matrix.

        :param matrix: Generated binary two-dimensional matrix.
                        The data of this matrix contains only 0 or 1 (non-char).
                        Type: int or bit.

        :return dna_motifs: The DNA motif of len(matrix) rows.
                             Type: list(list(char)).
        """
        dna_motifs = []

        for row in range(len(matrix)):
            self.m.output(row, len(matrix))
            dna_motifs.append(self.__list_to_motif__(self.__huffman_compressed__(matrix[row])))

        return dna_motifs

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
            current_number = int("".join(list(map(str, binary_list[list_index: list_index + 8]))), 2)
            huffman_code = self.huffman_tree[current_number]
            for code_index in range(len(huffman_code)):
                ternary_list.append(int(huffman_code[code_index]))

        return ternary_list

    def __list_to_motif__(self, one_list):
        """
        introduction: from one binary list to DNA motif.

        :param one_list: One binary list.
                          Type: int or bit.

        :return dna_motif: One DNA motif.
                            Type: List(char).
        """
        dna_motif = []
        last_base = "A"
        for col in range(len(one_list)):
            current_base = inherent.rotate_code.get(last_base)[one_list[col]]
            dna_motif.append(current_base)
            last_base = current_base

        return dna_motif

# ================================================= decode part ========================================================

    def decode(self, dna_motifs):
        """
        introduction: Decode DNA motifs to the data of binary file.

        :param dna_motifs: The DNA motif of len(matrix) rows.
                            Type: One-dimensional list(string).

        :return matrix: The binary matrix corresponding to the dna motifs.
                         Type: Two-dimensional list(int).
        """

        self.m.restore()
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Convert DNA motifs to binary matrix.")
        matrix = self.__get_binaries__(dna_motifs)

        self.m.restore()
        return matrix

    def __get_binaries__(self, dna_motifs):
        """
        introduction: Decode DNA motifs to the data of binary file.

        :param dna_motifs: The DNA motif of len(matrix) rows.
                            Type: One-dimensional list(string).

        :return matrix: The binary matrix corresponding to the dna motifs.
                         Type: Two-dimensional list(int).
        """
        matrix = []
        index_binary_length = int(len(str(bin(len(dna_motifs)))) - 2)

        for index in range(len(dna_motifs)):
            self.m.output(index, len(dna_motifs))
            matrix.append(self.__huffman_decompressed__(self.__motif_to_list__(dna_motifs[index]), index_binary_length))

        return matrix

    def __motif_to_list__(self, dna_motif):
        """
        introduction: Convert one DNA motif to one binary list.

        :param dna_motif: One DNA motif.
                           Type: List(char).

        :return one_list: One ternary Huffman coding list.
                           Type: int
        """
        one_list = []
        last_base = "A"

        for index in range(len(dna_motif)):
            one_list.append(inherent.rotate_code.get(last_base).index(dna_motif[index]))
            last_base = dna_motif[index]

        return one_list

    def __huffman_decompressed__(self, ternary_list, index_binary_length):
        """
        introduction: Conversion of ternary Huffman coding to binary coding.

        :param ternary_list: The ternary Huffman coding.

        :return binary_list: The binary list.
                              Type: list(int).
        """
        binary_list = []

        temp_ternary = ""
        for index in range(len(ternary_list)):
            temp_ternary += str(ternary_list[index])

            for tree_index in range(len(self.huffman_tree)):
                if temp_ternary == self.huffman_tree[tree_index]:
                    if len(binary_list) + 8 < self.segment_length + index_binary_length:
                        binary_list += list(map(int, list(str(bin(tree_index))[2:].zfill(8))))
                    else:
                        remaining_length = self.segment_length + index_binary_length - len(binary_list)
                        binary_list += list(map(int, list(str(bin(tree_index))[2:].zfill(remaining_length))))
                    temp_ternary = ""
                    break

        return binary_list
