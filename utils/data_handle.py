"""
Name: Data Handle

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s):
Conversion of DNA sequences and binary document
"""

import struct
import math
import sys
import os

import Chamaeleo.utils.log as log
import Chamaeleo.utils.monitor as monitor


# noinspection PyProtectedMember
def read_binary_from_all(path, segment_length=120, need_log=False):
    """
    introduction: Reading binary matrix from document.

    :param path: File path.
                  Type: string

    :param segment_length: The binary segment length used for DNA sequence generation.
                           Considering current DNA synthesis technique limitation,
                           we usually set 120 as default segment length.

    :param need_log: choose to output log file or not.

    :return matrix: A matrix in which each row represents a binary segment that will be used for DNA sequence generation.
                    Type: two-dimensional list(int)
    """

    m = monitor.Monitor()
    try:

        # Open selected file
        with open(path, mode="rb") as file:

            if need_log:
                log.output(
                    log.NORMAL,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Read binary matrix from file: " + path,
                )
            size = os.path.getsize(path)

            # Set init storage matrix
            matrix = [
                [0 for _ in range(segment_length)]
                for _ in range(math.ceil(size * 8 / segment_length))
            ]

            row = 0
            col = 0
            for byte_index in range(size):
                if need_log:
                    m.output(byte_index, size)
                # Read a file as bytes
                one_byte = file.read(1)
                element = list(
                    map(
                        int,
                        list(str(bin(struct.unpack("B", one_byte)[0]))[2:].zfill(8)),
                    )
                )
                for bit_index in range(8):
                    matrix[row][col] = element[bit_index]
                    col += 1
                    if col == segment_length:
                        col = 0
                        row += 1

        if int(len(str(bin(len(matrix)))) - 2) * 7 > segment_length:
            if need_log:
                log.output(
                    log.WARN,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "The proportion of index in whole sequence may be high. "
                    "It is recommended to increase the output DNA sequences' length or to divide the file into more segment pools",
                )

        return matrix, size
    except IOError:
        log.output(
            log.ERROR,
            str(__name__),
            str(sys._getframe().f_code.co_name),
            "The file selection operation was not performed correctly. Please execute the operation again!",
        )


# noinspection PyBroadException,PyProtectedMember
def write_all_from_binary(path, matrix, size, need_log=False):
    """
    introduction: Writing binary matrix to document.

    :param path: File path.
                  Type: string

    :param matrix: A matrix in which each row represents a binary segment that will be used for DNA sequence generation.
                    Type: two-dimensional list(int)

    :param size: This refers to file size, to reduce redundant bits when transferring DNA to binary files.
                  Type: int

    :param need_log: choose to output log file or not.
    """
    m = monitor.Monitor()

    try:
        with open(path, "wb+") as file:
            if need_log:
                log.output(
                    log.NORMAL,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Write file from binary matrix: " + path,
                )

            # Change bit to byte (8 -> 1), and write a file as bytes
            bit_index = 0
            temp_byte = 0
            for row in range(len(matrix)):
                if need_log:
                    m.output(row, len(matrix))
                for col in range(len(matrix[0])):
                    bit_index += 1
                    temp_byte *= 2
                    temp_byte += matrix[row][col]
                    if bit_index == 8:
                        if size >= 0:
                            file.write(struct.pack("B", int(temp_byte)))
                            bit_index = 0
                            temp_byte = 0
                            size -= 1
    except IOError:
        log.output(
            log.ERROR,
            str(__name__),
            str(sys._getframe().f_code.co_name),
            "The file selection operation was not performed correctly. Please execute the operation again!",
        )


# noinspection PyBroadException,PyProtectedMember
def read_dna_file(path, need_log=False):
    """
    introduction: Reading DNA sequence set from documents.

    :param path: File path.
                  Type: string

    :return dna_sequences: A corresponding DNA sequence string in which each row acts as a sequence.
                           Type: one-dimensional list(string)

    :param need_log: need output log.
    """

    m = monitor.Monitor()

    dna_sequences = []

    try:
        with open(path, "r") as file:
            if need_log:
                log.output(
                    log.NORMAL,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Read DNA sequences from file: " + path,
                )

            # Read current file by line
            lines = file.readlines()
            for index in range(len(lines)):
                if need_log:
                    m.output(index, len(lines))
                line = lines[index]
                dna_sequences.append([line[col] for col in range(len(line) - 1)])

        return dna_sequences
    except IOError:
        log.output(
            log.ERROR,
            str(__name__),
            str(sys._getframe().f_code.co_name),
            "The file selection operation was not performed correctly. Please execute the operation again!",
        )


# noinspection PyProtectedMember,PyBroadException
def write_dna_file(path, dna_sequences, need_log=False):
    """
    introduction: Writing DNA sequence set to documents.

    :param path: File path.
                  Type: string

    :param dna_sequences: Generated DNA sequences.
                          Type: one-dimensional list(string)

    :param need_log: choose to output log file or not.
    """

    m = monitor.Monitor()

    try:
        with open(path, "w") as file:
            if need_log:
                log.output(
                    log.NORMAL,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Write DNA sequences to file: " + path,
                )
            for row in range(len(dna_sequences)):
                if need_log:
                    m.output(row, len(dna_sequences))
                file.write("".join(dna_sequences[row]) + "\n")
        return dna_sequences
    except IOError:
        log.output(
            log.ERROR,
            str(__name__),
            str(sys._getframe().f_code.co_name),
            "The file selection operation was not performed correctly. Please execute the operation again!",
        )
