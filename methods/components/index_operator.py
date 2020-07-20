"""
Name: Processing the relationship between index and data

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) Integrate index (to binary) to binary data, one or all.
             (2) Divide index (to decimal) and binary data, one or all.
             (3) Arrange the scrambled data by indexes.
"""
import sys

import Chamaeleo.utils.monitor as monitor
import Chamaeleo.utils.log as log


# noinspection PyProtectedMember
def connect_all(matrix, need_log=False):
    """
    introduction: Integrate index and data from the two-dimensional matrix.

    :param matrix: Data from input.
                   Type: Two-dimensional list(int).

    :param need_log:

    :return new_matrix: Data for output.
                        Type: Two-dimensional list(int).
    """
    m = monitor.Monitor()
    index_binary_length = int(len(str(bin(len(matrix)))) - 2)

    if need_log:
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
            "Add index in the binary matrix.")

    new_matrix = []
    for row in range(len(matrix)):
        if need_log:
            m.output(row + 1, len(matrix))
        new_matrix.append(connect(row, matrix[row], index_binary_length))

    m.restore()

    del matrix, m

    return new_matrix


def connect(index, data, index_binary_length):
    """
    introduction: Integrate index and data, list 0100+111101010.

    :param index: The index of data.
                   Type: int.

    :param data: Data from input.
                  Type: One-dimensional list(int).

    :param index_binary_length: Length of binary index.
                                 Type: int.

    :return one_list: One binary string..
                       Type: One-dimensional list(int).
    """
    bin_index = list(map(int, list(str(bin(index))[2:].zfill(index_binary_length))))
    one_list = bin_index + data

    return one_list


# noinspection PyProtectedMember
def divide_all(matrix, need_log=False):
    """
    introduction: Separate data from indexes in binary strings.

    :param matrix: The DNA sequence of len(matrix) rows.
                   Type: Two-dimensional list(int).

    :param need_log: need output log.

    :returns index, datas: Obtained data sets and index sets in corresponding locations.
                            Type: One-dimensional list(int), Two-dimensional list(int).
    """
    m = monitor.Monitor()
    index_binary_length = int(len(str(bin(len(matrix)))) - 2)

    if need_log:
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
            "Divide index and data from binary matrix.")

    indexs = []
    datas = []

    for row in range(len(matrix)):
        if need_log:
            m.output(row + 1, len(matrix))
        index, data = divide(matrix[row], index_binary_length)
        indexs.append(index)
        datas.append(data)

    m.restore()

    del matrix, m

    return indexs, datas


def divide(one_list, index_binary_length):
    """
    introduction: Separate data from the index in a binary string.

    :param one_list: One binary string..
                      Type: One-dimensional list(int).

    :param index_binary_length: Length of binary index.
                                 Type: int.

    :returns index, data: Obtained data and index.
                           Type: int, One-dimensional list(int).
    """
    # Convert binary index to decimal.
    index = int("".join(list(map(str, one_list[:index_binary_length]))), 2)
    data = one_list[index_binary_length:]

    return index, data


# noinspection PyProtectedMember
def sort_order(indexes, data_set, need_log=False):
    """
    introduction: Restore data in order of index.

    :param indexes: The indexes of data set.

    :param data_set: The disordered data set, the locations of this are corresponding to parameter "index".

    :param need_log: need output log.

    :returns matrix: Binary list in correct order.
                      Type: Two-dimensional list(int).
    """
    m = monitor.Monitor()

    if need_log:
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
            "Restore data order according to index.")

    # additional information checker
    flag_index = 0
    if max(indexes) > len(indexes):
        while True:
            if flag_index + 1 not in indexes:
                # index to length
                flag_index += 1
                break
            flag_index += 1

    if need_log and flag_index > 0:
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
            "There are " + str(flag_index) + " required bit segments and " +
                   str(len(indexes) - flag_index) + " additional bit segments")

    # noinspection PyUnusedLocal
    if flag_index > 0:
        matrix = [[0 for _ in range(len(data_set[0]))] for _ in range(flag_index)]
    else:
        matrix = [[0 for _ in range(len(data_set[0]))] for _ in range(len(indexes))]

    for index in range(len(matrix)):
        matrix[index] = data_set[indexes.index(index)]
        if need_log:
            m.output(index + 1, len(matrix))

    m.restore()

    del indexes, data_set, m

    return matrix
