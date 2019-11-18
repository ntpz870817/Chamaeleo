"""
Name: Reed-Solomon Error Correction

Reference: Oz J, Naor A. Reed Solomon Encoder/Decoder on the StarCore™ SC140/SC1400 Cores, With Extended Examples[J]. 2003.
           https://blog.csdn.net/qq_29110265/article/details/86519879
           https://github.com/yuta1331/reedsolomon

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) Add Reed-Solomon error correction for origin matrix or origin list.
             (2) Remove Reed-Solomon error correction from origin matrix or origin list.
             (2) Verify the correctness of the matrix or the list and repair the error information to a certain extent.
"""

import Chamaeleo.utils.log as log


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyTypeChecker,PyUnresolvedReferences
class RS:
    def __init__(self, check_size=3, need_log=False):
        """
        introduction: The initialization method of Reed-Solomon Codec.

        :param check_size: Check size of Reed-Solomon Codec.
        """
        self.check_size = check_size
        self.galois_field_exp, self.galois_field_log = self.__init_galois_field__()
        self.rs_generator = self.__obtain_generator__()
        self.length_examine = False
        self.need_log = need_log

    def __init_galois_field__(self):
        """
        introduction: Init Galois Field exp and log.
        """
        galois_field_exp = [1] * 512
        galois_field_log = [0] * 256
        value = 1
        for index in range(1, 255):
            value <<= 1
            if value & 0x100:
                value ^= 0x11D
            galois_field_exp[index] = value
            galois_field_log[value] = index
        for index in range(255, 512):
            galois_field_exp[index] = galois_field_exp[index - 255]

        return galois_field_exp, galois_field_log

    def add_for_matrix(self, matrix):
        """
        introduction: Add Reed-Solomon error correction for origin matrix.

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

        if len(matrix[0]) / 8 + self.check_size > 255:
            if self.need_log:
                log.output(
                    log.WARN,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Data length is too long, encoding and decoding will take a lot of time.",
                )
        self.length_examine = True

        verify_matrix = []
        for row in range(len(matrix)):
            verify_matrix.append(self.add_for_list(matrix[row]))
        return verify_matrix

    # noinspection PyUnusedLocal
    def add_for_list(self, input_list):
        """
        introduction: Add Reed-Solomon error correction for a origin list.

        :param input_list: Origin list.
                           The data of this matrix contains only 0 or 1 (non-char).
                           Type: One-dimensional list(int).

        :return output_list: The binary list completing processing.
                             The data of this matrix contains only 0 or 1 (non-char).
                             Type: One-dimensional list(int).
        """
        if len(input_list) / 8 + self.check_size > 255:
            if self.length_examine is False:
                if self.need_log:
                    log.output(
                        log.WARN,
                        str(__name__),
                        str(sys._getframe().f_code.co_name),
                        "Data length is too long, encoding and decoding will take a lot of time.",
                    )

        if len(input_list) % 8 != 0:
            add_length = 8 - len(input_list) % 8
            input_list = [0 for add_bit in range(add_length)] + input_list

        input_list = self.__binary_to_decimal__(input_list)
        output_list = [0] * (len(input_list) + self.check_size)
        output_list[: len(input_list)] = input_list
        for data_index in range(len(input_list)):
            coefficient = output_list[data_index]
            if coefficient != 0:
                for rs_index in range(len(self.rs_generator)):
                    output_list[
                        data_index + rs_index
                    ] ^= self.__galois_field_multiply__(
                        self.rs_generator[rs_index], coefficient
                    )
        output_list[: len(input_list)] = input_list
        output_list = self.__decimal_to_binary__(output_list)
        return output_list

    def remove_for_matrix(self, verity_matrix, original_length):
        """
        introduction: Remove Reed-Solomon error correction from origin matrix.

        :param verity_matrix: Verifiable matrix.
                              The data of this matrix contains only 0 or 1 (non-char).
                              Type: Two-dimensional list(int).

        :param original_length:

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
            matrix.append(self.remove_for_list(verity_matrix[row], original_length))
        return matrix

    def remove_for_list(self, input_list, original_length):
        """
        introduction: Remove Reed-Solomon error correction from origin list.

        :param input_list: Verifiable list.
                            The data of this matrix contains only 0 or 1 (non-char).
                            Type: One-dimensional list(int).

        :param original_length:

        :return output_list: Origin list.
                             Type: One-dimensional list(int).
        """
        output_list = input_list[: -self.check_size * 8]
        output_list = output_list[len(output_list) - original_length:]
        return output_list

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

    def verify_for_list(self, input_list, row=None):
        """
        introduction: Verify the correctness of the list and repair the error information to a certain extent.

        :param input_list: Verifiable list.
                            The data of this matrix contains only 0 or 1 (non-char).
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

        output_list = self.__binary_to_decimal__(input_list)
        # find erasures
        erasure_positions = []
        for index in range(len(output_list)):
            if output_list[index] < 0:
                output_list[index] = 0
                erasure_positions.append(index)
        if len(erasure_positions) > self.check_size:
            if row is not None:
                log.output(
                    log.ERROR,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Row" + str(row) + " has too many erasures to correct!",
                )
            else:
                log.output(
                    log.ERROR,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Too many erasures to correct!",
                )

        syndromes = [
            self.__galois_field_evaluate__(output_list, self.galois_field_exp[i])
            for i in range(self.check_size)
        ]
        if max(syndromes) == 0:
            output_list = self.__decimal_to_binary__(output_list)
            return output_list

        forney_syndromes = self.__forney_syndromes__(
            syndromes, erasure_positions, len(output_list)
        )
        error_positions = self.__find_errors__(forney_syndromes, len(output_list), row)
        if erasure_positions is None:
            output_list = self.__decimal_to_binary__(output_list)
            return output_list

        if error_positions is None:
            error_positions = []
        output_list = self.__correct_errata__(
            output_list, syndromes, erasure_positions + error_positions
        )
        if (
            max(
                [
                    self.__galois_field_evaluate__(
                        output_list, self.galois_field_exp[i]
                    )
                    for i in range(self.check_size)
                ]
            )
            > 0
        ):
            if row is not None:
                log.output(
                    log.ERROR,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Row" + str(row) + "could not be correct!",
                )
            else:
                log.output(
                    log.ERROR,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Could not be correct!",
                )
        output_list = self.__decimal_to_binary__(output_list)
        return output_list

    # ================================================= other parts ========================================================

    def __binary_to_decimal__(self, binary):
        """
        introduction: Convert binary array to decimal array using bytes as units

        :param binary: Binary array.
                       The data of this array contains only 0 or 1 (non-char).
                       Type: One-dimensional list(bit)

        :return decimal: Decimal array.
                        Type: One-dimensional list(int)
        """
        decimal = []
        for index in range(0, len(binary), 8):
            decimal.append(int("".join(list(map(str, binary[index: index + 8]))), 2))
        return decimal

    def __decimal_to_binary__(self, decimal):
        """
        introduction: Convert decimal array to binary array using bytes as units

        :param decimal: Decimal array.
                        The data of this array contains only 0 or 1 (non-char).
                        Type: One-dimensional list(int)

        :return binary: Binary array.
                        The data of this array contains only 0 or 1 (non-char).
                        Type: One-dimensional list(bit)
        """
        binary = []
        for index in range(len(decimal)):
            binary += list(map(int, list(str(bin(decimal[index]))[2:].zfill(8))))
        return binary

    def __obtain_generator__(self):
        """
        introduction: Obtain Reed-Solomon matrix generator.

        :return generator: Reed-Solomon matrix generator.
        """
        generator = [1]
        for index in range(self.check_size):
            generator = self.__galois_field_polynomial_multiply__(
                generator, [1, self.galois_field_exp[index]]
            )
        return generator

    def __forney_syndromes__(self, syndromes, erasure_positions, length):
        """
        introduction:

        :param syndromes:

        :param erasure_positions:

        :param length:

        :return forney_syndromes:
        """
        forney_syndromes = list(syndromes)
        for index in range(len(erasure_positions)):
            value = self.galois_field_exp[length - 1 - erasure_positions[index]]
            for j in range(len(forney_syndromes) - 1):
                forney_syndromes[j] = (
                    self.__galois_field_polynomial_multiply__(
                        forney_syndromes[j], value
                    )
                    ^ forney_syndromes[j + 1]
                )
            forney_syndromes.pop()

        return forney_syndromes

    def __find_errors__(self, syndromes, length, row=None):
        """
        introduction: Find error locator polynomial with Berlekamp-Massey algorithm.

        :param syndromes:

        :param length:

        :return error_positions:
        """
        error_polynomial = [1]
        old_polynomial = [1]
        for index in range(0, len(syndromes)):
            old_polynomial.append(0)
            delta = syndromes[index]
            for position in range(1, len(error_polynomial)):
                delta ^= self.__galois_field_multiply__(
                    error_polynomial[len(error_polynomial) - 1 - position],
                    syndromes[index - position],
                )
            if delta != 0:
                if len(old_polynomial) > len(error_polynomial):
                    new_polynomial = self.__galois_field_scale__(old_polynomial, delta)
                    old_polynomial = self.__galois_field_scale__(
                        error_polynomial, self.__galois_field_division__(1, delta)
                    )
                    error_polynomial = new_polynomial
                error_polynomial = self.__galois_field_add__(
                    error_polynomial, self.__galois_field_scale__(old_polynomial, delta)
                )

        errors = len(error_polynomial) - 1
        if errors * 2 > len(syndromes):
            if row is not None:
                log.output(
                    log.ERROR,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Row" + str(row) + " has too many erasures to correct!",
                )
            else:
                log.output(
                    log.ERROR,
                    str(__name__),
                    str(sys._getframe().f_code.co_name),
                    "Too many erasures to correct!",
                )
        # find zeros of error polynomial
        error_positions = []
        for index in range(length):
            if (
                self.__galois_field_evaluate__(
                    error_polynomial, self.galois_field_exp[255 - index]
                )
                == 0
            ):
                error_positions.append(length - 1 - index)
        if len(error_positions) != errors:
            # couldn't find error locations
            return None
        return error_positions

    def __correct_errata__(self, input_list, syndromes, positions):
        """
        introduction: Calculate error locator polynomial.

        :param input_list:

        :param syndromes:

        :param positions:

        :return input_list:
        """
        locators = [1]
        for index in range(len(positions)):
            value = self.galois_field_exp[len(input_list) - 1 - positions[index]]
            locators = self.__galois_field_polynomial_multiply__(locators, [value, 1])

        # calculate error evaluator polynomial
        polynomial = syndromes[0 : len(positions)]
        polynomial.reverse()
        polynomial = self.__galois_field_polynomial_multiply__(polynomial, locators)
        polynomial = polynomial[len(polynomial) - len(positions) : len(polynomial)]

        # formal derivative of error locator eliminates even terms
        locators = locators[len(locators) & 1 : len(locators) : 2]
        # compute corrections
        for index in range(0, len(positions)):
            value1 = self.galois_field_exp[positions[index] + 256 - len(input_list)]
            value2 = self.__galois_field_evaluate__(polynomial, value1)
            value3 = self.__galois_field_evaluate__(
                locators, self.__galois_field_multiply__(value1, value1)
            )
            value4 = self.__galois_field_multiply__(value1, value3)
            input_list[positions[index]] ^= self.__galois_field_division__(
                value2, value4
            )

        return input_list

    def __galois_field_add__(self, galois_field_1, galois_field_2):
        """
        introduction:

        :param galois_field_1:

        :param galois_field_2:

        :return result:
        """
        result = [0] * max(len(galois_field_1), len(galois_field_2))
        for index in range(len(galois_field_1)):
            result[index + len(result) - len(galois_field_1)] = galois_field_1[index]
        for index in range(len(galois_field_2)):
            result[index + len(result) - len(galois_field_2)] ^= galois_field_2[index]
        return result

    def __galois_field_multiply__(self, value1, value2):
        """
        introduction:

        :param value1:

        :param value2:

        :return result:
        """
        if value1 == 0 or value2 == 0:
            return 0
        return self.galois_field_exp[
            self.galois_field_log[value1] + self.galois_field_log[value2]
        ]

    def __galois_field_polynomial_multiply__(self, galois_field_1, galois_field_2):
        result = [0] * (len(galois_field_1) + len(galois_field_2) - 1)
        for index_2 in range(0, len(galois_field_2)):
            for index_1 in range(0, len(galois_field_1)):
                if galois_field_1[index_1] == 0 or galois_field_2[index_2] == 0:
                    result[index_1 + index_2] ^= 0
                else:
                    result[index_1 + index_2] ^= self.__galois_field_multiply__(
                        galois_field_1[index_1], galois_field_2[index_2]
                    )
        return result

    def __galois_field_division__(self, value1, value2):  # x / y on gf_exp
        """
        introduction:

        :param value1:

        :param value2:

        :return result:
        """
        if value2 == 0:
            raise ZeroDivisionError()
        if value1 == 0:
            return 0
        return self.galois_field_exp[
            self.galois_field_log[value1] + 255 - self.galois_field_log[value2]
        ]

    def __galois_field_scale__(self, galois_field, value):
        """
        introduction:

        :param galois_field:

        :param value:

        :return result:
        """
        # p_list * x on gf_exp # [(p[0] * x), (p[1] * x), ...]
        return [
            self.__galois_field_multiply__(galois_field[i], value)
            for i in range(0, len(galois_field))
        ]

    def __galois_field_evaluate__(self, galois_field, value):
        """
        introduction:

        :param galois_field:

        :param value:

        :return new_galois_field:
        """
        new_galois_field = galois_field[0]
        for index in range(1, len(galois_field)):
            new_value = self.galois_field_exp[
                self.galois_field_log[new_galois_field] + self.galois_field_log[value]
            ]
            new_galois_field = new_value ^ galois_field[index]
        return new_galois_field
