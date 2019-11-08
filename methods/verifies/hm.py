"""
Name: Hamming Error Correction

Reference: Wei V K. Generalized Hamming weights for linear codes[J]. IEEE Transactions on information theory, 1991, 37(5): 1412-1418.

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) Add Hamming error correction for origin matrix or origin list.
             (2) Remove Hamming error correction from origin matrix or origin list.
             (2) Verify the correctness of the matrix or the list and repair the error information to a certain extent.
"""
import sys

import Chamaeleo.utils.log as log


# noinspection PyProtectedMember,PyMethodMayBeStatic
class Hm:
    def __init__(self, need_log=False):
        self.need_log = need_log

    def add_for_matrix(self, matrix):
        """
        introduction: Add Hamming error correction for origin matrix.

        :param matrix: Origin matrix.
                       The data of this matrix contains only 0 or 1 (non-char).
                       Type: Two-dimensional list(int).

        :return verity_matrix: Verifiable matrix.
                               Type: Two-dimensional list(int).
        """
        if self.need_log:
            log.output(
                log.NORMAL,
                str(__name__),
                str(sys._getframe().f_code.co_name),
                "Add the error correction for matrix.",
            )

        # Calculate the length needed for detection site.
        detect_site_length = 0
        while (len(matrix[0]) + detect_site_length + 1) > (pow(2, detect_site_length)):
            detect_site_length += 1

        verity_matrix = []

        for row in range(len(matrix)):
            verity_matrix.append(self.add_for_list(matrix[row], detect_site_length))

        return verity_matrix

    def add_for_list(self, input_list, detect_site_length=None):
        """
        introduction: Add Hamming error correction for one list.

        :param input_list: The binary list requiring additional validation.
                           Type: One-dimensional list(int).

        :param detect_site_length: The length of detection site.

        :return output_list: The binary list completing processing.
                             Type: One-dimensional list(int).
        """
        if detect_site_length is None:
            # Calculate the length needed for detection site.
            detect_site_length = 0
            while (len(input_list) + detect_site_length + 1) > (
                pow(2, detect_site_length)
            ):
                detect_site_length += 1

        input_list.reverse()

        # Add detection site in the origin list.
        detect_site, list_site, output_list = 0, 0, []
        for index in range(detect_site_length + len(input_list)):
            if pow(2, detect_site) == index + 1:
                output_list.append(0)
                detect_site += 1
            else:
                output_list.append(input_list[list_site])
                list_site += 1

        # XOR operations on each detection site
        # From the 2^(k - 1) bit of the new code, the k-bit parity-check code calculates
        # the exclusive or of 2^(k - 1) bits, jumps 2^(k - 1) bits,
        # calculates the exclusive or of the next set of 2^(k - 1) bits, and fills in 2^(k - 1) bits.
        detect_site = 0
        for parity in range(len(output_list)):
            if pow(2, detect_site) == parity + 1:
                start_index = pow(2, detect_site) - 1
                index = start_index
                xor = []

                while index < len(output_list):
                    xor.extend(output_list[index : index + pow(2, detect_site)])
                    index += pow(2, detect_site + 1)

                for xor_index in range(1, len(xor)):
                    output_list[start_index] = output_list[start_index] ^ xor[xor_index]
                detect_site += 1

        output_list.reverse()

        return output_list

    def remove_for_matrix(self, verity_matrix):
        """
        introduction: Remove Hamming error correction from origin matrix.

        :param verity_matrix: Verifiable matrix.
                              The data of this matrix contains only 0 or 1 (non-char).
                              Type: Two-dimensional list(int).

        :return matrix: Origin matrix.
                        Type: Two-dimensional list(int).
        """
        if self.need_log:
            log.output(
                log.NORMAL,
                str(__name__),
                str(sys._getframe().f_code.co_name),
                "Remove the error correction for matrix.",
            )
        matrix = []
        for row in range(len(verity_matrix)):
            matrix.append(self.remove_for_list(verity_matrix[row]))
        return matrix

    def remove_for_list(self, input_list):
        """
        introduction: Remove Hamming error correction from one list.

        :param input_list: The binary list requiring removing validation.
                           Type: One-dimensional list(int).

        :return output_list: The binary list completing processing.
                             Type: One-dimensional list(int).
        """
        input_list.reverse()

        detect_site, output_list = 0, []
        # Remove the detection site.
        for index in range(len(input_list)):
            if pow(2, detect_site) == index + 1:
                detect_site += 1
            else:
                output_list.append(input_list[index])

        output_list.reverse()

        return output_list

    # noinspection PyProtectedMember
    def verify_for_matrix(self, verity_matrix):
        """
        introduction: Verify the correctness of the matrix and repair the error information to a certain extent.

        :param verity_matrix: Matrix waiting for validation.
                              Type: Two-dimensional list(int).

        :return matrix: Matrix that has been verified even repaired.
                        Type: Two-dimensional list(int).
        """
        if self.need_log:
            log.output(
                log.NORMAL,
                str(__name__),
                str(sys._getframe().f_code.co_name),
                "Verify and repair the matrix.",
            )

        matrix = []
        for row in range(len(verity_matrix)):
            matrix.append(self.verify_for_list(verity_matrix[row], row))

        return matrix

    # noinspection PyProtectedMember
    def verify_for_list(self, input_list, row=None):
        """
        introduction: Verify the correctness of the list and repair the error information to a certain extent.

        :param input_list: The binary list requiring validation.
                           Type: One-dimensional list(int).

        :param row: The number of rows of the matrix to which the list belongs.

        :return output_list: List that has been verified even repaired.
                             Type: One-dimensional list(int).
        """
        if row is None:
            if self.need_log:
                log.output(
                    log.NORMAL,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Verify and repair the list.",
                )

        input_list.reverse()
        detect_site, output_list, output_list_copy = 0, [], []
        for index in range(0, len(input_list)):
            output_list.append(input_list[index])
            output_list_copy.append(input_list[index])
            if pow(2, detect_site) == index + 1:
                detect_site += 1

        detect_site, parity_list = 0, []
        for parity in range(0, (len(output_list))):
            if pow(2, detect_site) == parity + 1:
                start_index = pow(2, detect_site) - 1
                index = start_index
                xor = []

                while index < len(output_list):
                    block = output_list[index : index + pow(2, detect_site)]
                    xor.extend(block)
                    index += pow(2, detect_site + 1)

                for xor_index in range(1, len(xor)):
                    output_list[start_index] = output_list[start_index] ^ xor[xor_index]
                parity_list.append(output_list[parity])
                detect_site += 1
        parity_list.reverse()
        error = sum(
            int(parity_list) * pow(2, index)
            for index, parity_list in enumerate(parity_list[::-1])
        )

        if error == 0:
            input_list.reverse()
            return input_list
        elif error >= len(output_list_copy):
            log.output(
                log.ERROR,
                str(__name__),
                str(sys._getframe().f_code.co_name),
                "Error cannot be detected.",
            )
        else:
            if self.need_log:
                if row is not None:
                    log.output(
                        log.WARN,
                        str(__name__),
                        str(sys._getframe().f_code.co_name),
                        "Error is No. "
                        + str(len(output_list_copy) - error)
                        + "bit, in "
                        + str(row + 1)
                        + " of matrix, and it is repaired.",
                    )
                else:
                    log.output(
                        log.WARN,
                        str(__name__),
                        str(sys._getframe().f_code.co_name),
                        "Error is No. " + str(len(output_list_copy) - error) + "bit, and it is repaired.",
                    )

            if output_list_copy[error - 1] == 0:
                output_list_copy[error - 1] = 1
            else:
                output_list_copy[error - 1] = 0
            # output_list_copy[error - 1] = int(output_list_copy[error - 1] is False)
            output_list_copy.reverse()
            return output_list_copy
