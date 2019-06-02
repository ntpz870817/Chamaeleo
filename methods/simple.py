"""
Name: Simple (Simple DNA Storage Code)

Reference: Church G M, Gao Y, Kosuri S. Next-generation digital information storage in DNA[J]. Science, 2012, 337(6102): 1628-1628.

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) DNA encoding by Simple.
             (2) DNA decoding by Simple.
"""

import sys
import random

import utils.monitor as monitor
import utils.log as log
import methods.property.inherent as inherent


# noinspection PyMethodMayBeStatic,PyProtectedMember
class Simple:
    def __init__(self, mapping_rule=None):
        """
        introduction: The initialization method of Simple.

        :param mapping_rule: Mapping between bases and numbers.
                              There can be two settings:
                              (1) Two bases correspond to a number (0 or 1): i.e. AT-0, CG-1.
                              (2) Each base corresponds to a number: i.e. A-00, T-01, C-10, G-11.
        """

        if not mapping_rule:
            mapping_rule = [0, 0, 1, 1]
        else:
            self.__init_check__(mapping_rule)

        self.mapping_rule = mapping_rule
        self.file_size = 0
        self.index_binary_length = 0
        self.monitor = monitor.Monitor()

    def __init_check__(self, mapping_rule):
        """
        introduction: The verification of initialization parameters.

        :param mapping_rule: Mapping between bases and numbers.
                              There can be two settings:
                              (1) Two bases correspond to a number (0 or 1): i.e. AT-0, CG-1.
                              (2) Each base corresponds to a number: i.e. A-00, T-01, C-10, G-11.
        """

        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Create the Simple method.")

        if 0 <= max(mapping_rule) <= 1:
            if len([position for position, value in enumerate(mapping_rule) if value == 0]) != 2 \
                    or [position for position, value in enumerate(mapping_rule) if value == 1] != 2:
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "mapping rule is wrong!")
            else:
                pass
        else:
            if (0 in mapping_rule) and (1 in mapping_rule) and (2 in mapping_rule) and (3 in mapping_rule):
                pass
            else:
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "mapping rule is wrong!")

# ================================================= encode part ========================================================

    def encode(self, matrix, file_size):
        """
        introduction: Encode DNA motifs from the data of binary file.

        :param matrix: Generated binary two-dimensional matrix.
                        The data of this matrix contains only 0 or 1 (non-char).
                        Type: int or bit.

        :param file_size: The size of the file corresponds to this matrix.

        :return dna_motifs: The DNA motif of len(matrix) rows.
                             Type: list(list(char)).
        """

        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Encode the file.")

        self.monitor.restore()

        self.file_size = file_size
        self.index_binary_length = int(len(str(bin(len(matrix)))) - 2)

        dna_motifs = []
        for row in range(len(matrix)):
            self.monitor.output(row, len(matrix))
            dna_motifs.append(self.__list_to_motif__(list(map(int, list(str(bin(row))[2:].zfill(self.index_binary_length)))) + matrix[row]))

        return dna_motifs

    def __list_to_motif__(self, one_list):
        """
        introduction: from one binary list to DNA motif.

        :param one_list: One binary list.
                          Type: int or bit.

        :return: One DNA motif.
                  Type: List(char).
        """
        dna_motif = []
        if max(self.mapping_rule) == 3:
            if len(one_list) % 2 != 0:
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "Data length cannot be odd number!")
            for index in range(len(one_list)):
                dna_motif.append(inherent.index_base.get(self.mapping_rule.index(one_list[index] * 2 + one_list[index + 1])))
        else:
            for index in range(len(one_list)):
                options = [position for position, value in enumerate(self.mapping_rule) if value == one_list[index]]
                dna_motif.append(inherent.index_base.get(random.choice(options)))
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
        self.monitor.restore()

        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Convert DNA motifs to binary matrix.")
        temp_matrix = []
        for index in range(len(dna_motifs)):
            self.monitor.output(index, len(dna_motifs))
            temp_matrix.append(self.__motif_to_list__(dna_motifs[index]))

        self.monitor.restore()

        self.monitor.restore()
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Divide index and data from binary matrix.")
        indexs, datas = self.__divide_indexs_datas__(temp_matrix)

        self.monitor.restore()
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Restore the disrupted data order.")
        matrix = self.__sort_order__(indexs, datas)

        self.monitor.restore()

        return matrix

    def __motif_to_list__(self, dna_motif):
        """
        introduction: Convert one DNA motif to one binary list.

        :param dna_motif: One DNA motif.
                           Type: String.

        :return one_list: The binary list corresponding to the dna motif.
                           Type: One-dimensional list(int).
        """
        one_list = []
        if max(self.mapping_rule) == 3:
            for index in range(len(dna_motif)):
                number = self.mapping_rule[inherent.base_index.get(dna_motif[index])]
                one_list.append(1 if number >= 2 else 0)
                one_list.append(1 if number % 2 == 1 else 0)
        else:
            for index in range(len(dna_motif)):
                one_list.append(self.mapping_rule[inherent.base_index.get(dna_motif[index])])

        return one_list

    def __divide_indexs_datas__(self, matrix):
        """
        introduction: Separate data from indexes in binary strings.

        :param matrix: The DNA motif of len(matrix) rows.
                        Type: Two-dimensional list(int).

        :returns index, datas: Obtained data sets and index sets in corresponding locations.
                                Type: One-dimensional list(int), Two-dimensional list(int).
        """

        indexs = []
        datas = []

        for row in range(len(matrix)):
            self.monitor.output(row, len(matrix))
            # Convert binary index to decimal.
            index = int("".join(list(map(str, matrix[row][:self.index_binary_length]))), 2)

            indexs.append(index)
            datas.append(matrix[row][self.index_binary_length:])

        del matrix

        return indexs, datas

    # noinspection PyUnusedLocal
    def __sort_order__(self, indexs, datas):
        """
        introduction: Restore data in order of index.

        :param indexs: The indexes of data set.

        :param datas: The disordered data set, the locations of this are corresponding to parameter "index".

        :returns matrix: Binary list in correct order.
                          Type: Two-dimensional list(int).
        """

        matrix = [[0 for col in range(len(datas[0]))] for row in range(len(indexs))]

        for row in range(len(indexs)):
            self.monitor.output(row, len(indexs))
            if 0 <= row < len(matrix):
                matrix[indexs[row]] = datas[row]

        del indexs, datas

        return matrix