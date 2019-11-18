"""
Name: Processing the relationship between index and data

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) Connect index (to binary) to binary data, one or all.
             (2) Divide index (to decimal) and binary data, one or all.
             (3) Arrange the scrambled data by indexes.
"""
import sys

import Chamaeleo.utils.monitor as monitor
import Chamaeleo.utils.log as log


# noinspection PyProtectedMember
def connect_all(matrix, need_log=False):
    """
    introduction: Connect index and data from the two-dimensional matrix.

    :param matrix: Data from input.
                   Type: Two-dimensional list(int).

    :return new_matrix: Data for output.
                        Type: Two-dimensional list(int).
    """
    m = monitor.Monitor()
    index_binary_length = int(len(str(bin(len(matrix)))) - 2)

    if need_log:
        log.output(
            log.NORMAL,
            str(__name__),
            str(sys._getframe().f_code.co_name),
            "Add index in the binary matrix.",
        )

    new_matrix = []
    for row in range(len(matrix)):
        m.output(row, len(matrix))
        new_matrix.append(connect(row, matrix[row], index_binary_length))

    m.restore()

    del matrix, m

    return new_matrix


def connect(index, data, index_binary_length):
    """
    introduction: Connect index and data, list 0100+111101010.

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

    :param matrix: The DNA motif of len(matrix) rows.
                   Type: Two-dimensional list(int).

    :returns index, datas: Obtained data sets and index sets in corresponding locations.
                            Type: One-dimensional list(int), Two-dimensional list(int).
    """
    m = monitor.Monitor()
    index_binary_length = int(len(str(bin(len(matrix)))) - 2)

    if need_log:
        log.output(
            log.NORMAL,
            str(__name__),
            str(sys._getframe().f_code.co_name),
            "Divide index and data from binary matrix.",
        )

    indexs = []
    datas = []

    for row in range(len(matrix)):
        m.output(row, len(matrix))
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

    :returns matrix: Binary list in correct order.
                      Type: Two-dimensional list(int).
    """
    m = monitor.Monitor()

    if need_log:
        log.output(
            log.NORMAL,
            str(__name__),
            str(sys._getframe().f_code.co_name),
            "Restore the disrupted data order.",
        )

    # noinspection PyUnusedLocal
    matrix = [[0 for col in range(len(data_set[0]))] for row in range(len(indexes))]

    for row in range(len(indexes)):
        m.output(row, len(indexes))
        if 0 <= row < len(matrix):
            matrix[indexes[row]] = data_set[row]

    m.restore()

    del indexes, data_set, m

    return matrix
