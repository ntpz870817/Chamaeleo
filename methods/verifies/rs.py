"""
Name: Reed-Solomon Error Correction

Reference:
Oz J, Naor A. Reed Solomon Encoder/Decoder on the StarCore™ SC140/SC1400 Cores, With Extended Examples[J]. 2003.
https://github.com/yuta1331/reedsolomon

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s):
(1) Add Reed-Solomon error correction for origin matrix or origin list.
(2) Remove Reed-Solomon error correction from origin matrix or origin list.
(3) Verify the correctness of the matrix or the list and repair the error information to a certain extent.
"""
import sys
import platform
import Chamaeleo.utils.log as log
from Chamaeleo.utils import monitor
from reedsolo import RSCodec, ReedSolomonError


# noinspection PyProtectedMember
class RS:
    def __init__(self, check_size=3, additional_size=None):
        """
        introduction: The initialization method of Reed-Solomon Codec.

        :param check_size: Check size of Reed-Solomon Codec.

        :param additional_size: The additional size for length completion mentioned in encoding process of RS code.
        """
        self.check_size = check_size
        if additional_size is not None:
            self.additional_size = additional_size
        else:
            self.additional_size = 0

        self.m = monitor.Monitor()
        self.tool = RSCodec(check_size)

    def add_for_matrix(self, matrix, need_log=False):
        """
        introduction: Add Reed-Solomon error correction for origin matrix.

        :param matrix: Origin matrix.
                       The data of this matrix contains only 0 or 1 (non-char).
                       Type: Two-dimensional list(int).

        :param need_log: Show the log.

        :return verity_matrix: Verifiable matrix.
                               Type: Two-dimensional list(int).
        """
        if need_log:
            log.output(
                log.NORMAL,
                str(__name__),
                str(sys._getframe().f_code.co_name),
                "Add the error correction for matrix.",
            )

        if len(matrix[0]) / 8 + self.check_size > 255:
            log.output(
                log.WARN,
                str(__name__),
                str(sys._getframe().f_code.co_name),
                "Data length is too long, encoding and decoding will take a lot of time.",
            )

        self.additional_size = 8 - len(matrix[0]) % 8
        log.output(
            log.WARN,
            str(__name__),
            str(sys._getframe().f_code.co_name),
            "Data has additional length: " + str(self.additional_size) + ".",
        )

        self.m.restore()

        verify_matrix = []
        for row in range(len(matrix)):
            if need_log:
                self.m.output(row, len(matrix))
            verify_matrix.append(self.add_for_list(matrix[row], row))

        self.m.restore()

        return verify_matrix

    # noinspection PyUnusedLocal
    def add_for_list(self, input_list, row=None, need_log=False):
        """
        introduction: Add Reed-Solomon error correction for a origin list.

        :param input_list: Origin list.
                           The data of this matrix contains only 0 or 1 (non-char).
                           Type: One-dimensional list(int).

        :param row: The number of rows of the matrix to which the list belongs.

        :param need_log: Show the log.

        :return output_list: The binary list completing processing.
                             The data of this matrix contains only 0 or 1 (non-char).
                             Type: One-dimensional list(int).
        """
        if need_log:
            log.output(
                log.NORMAL,
                str(__name__),
                str(sys._getframe().f_code.co_name),
                "Add the error correction for list.",
            )

        if row is None:
            self.additional_size = 8 - len(input_list) % 8
            log.output(
                log.WARN,
                str(__name__),
                str(sys._getframe().f_code.co_name),
                "Data has additional length: " + str(self.additional_size) + ".",
            )

        input_list = [0 for add_bit in range(self.additional_size)] + input_list

        byte_list = []
        for index in range(0, len(input_list), 8):
            byte_list.append(int(str("".join(list(map(str, input_list[index: index + 8])))), 2))

        output_list = []
        for one_byte in list(self.tool.encode(byte_list)):
            temp_bits = list(map(int, list(bin(one_byte))[2:]))
            temp_bits = [0 for _ in range(8 - len(temp_bits))] + temp_bits
            output_list += temp_bits

        return output_list

    def verify_for_matrix(self, verity_matrix, need_log=False):
        """
        introduction: Verify the correctness of the matrix and repair the error information to a certain extent.

        :param verity_matrix: Matrix waiting for validation.
                              Type: Two-dimensional list(int).

        :param need_log: Show the log.

        :return matrix: Matrix that has been verified even repaired.
                        Type: Two-dimensional list(int).
        """
        if need_log:
            log.output(
                log.NORMAL,
                str(__name__),
                str(sys._getframe().f_code.co_name),
                "Verify and repair the matrix.",
            )

        self.m.restore()

        matrix = []
        for row in range(len(verity_matrix)):
            if need_log:
                self.m.output(row, len(verity_matrix))
            matrix.append(self.verify_for_list(verity_matrix[row], row))

        self.m.restore()

        return matrix

    def verify_for_list(self, input_list, row=None, need_log=False):
        """
        introduction: Verify the correctness of the list and repair the error information to a certain extent.

        :param input_list: Verifiable list.
                            The data of this matrix contains only 0 or 1 (non-char).
                            Type: One-dimensional list(int).

        :param row: The number of rows of the matrix to which the list belongs.

        :param need_log: Show the log.

        :return output_list: List that has been verified even repaired.
                             Type: One-dimensional list(int).
        """
        if row is None:
            if need_log:
                log.output(
                    log.NORMAL,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Verify and repair the list.",
                )

        byte_list = []
        for index in range(0, len(input_list), 8):
            byte_list.append(int(str("".join(list(map(str, input_list[index: index + 8])))), 2))

        try:
            decode_byte_list = list(self.tool.decode(byte_list))

            if platform.system() == "Linux":
                decode_byte_list = decode_byte_list[0]

            output_list = []
            for one_byte in list(decode_byte_list):
                temp_bits = list(map(int, list(bin(one_byte))[2:]))
                temp_bits = [0 for _ in range(8 - len(temp_bits))] + temp_bits
                output_list += temp_bits
        except ReedSolomonError:
            return None

        output_list = output_list[self.additional_size:]

        return output_list
