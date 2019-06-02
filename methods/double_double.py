"""
Name: DDC (Double-Double DNA Storage Code)

Reference: None

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) DNA encoding by DDYYC.
             (2) DNA decoding by DDYYC.

Advantages: (1) High compressibility, maximum compressibility to 1/2 of the original data.
            (2) Prevent repetitive motifs, like ATCGATCG...
            (3) Increase the number of sequence changes (far exceed YYC, 5,566,277,615,616 cases), increasing data security.
"""

import sys

import methods.yin_yang as yyc
import utils.log as log


# noinspection PyProtectedMember
class DDC(yyc.YYC):

    def __init_check__(self, support_bases, support_spacing, base_reference, current_code_matrix, max_ratio):
        """
        introduction: The verification of initialization parameters in DDC.

        :param base_reference: Correspondence between base and binary data (RULE 1).
                                Make sure that Two of the bases are 1 and the other two are 0.

        :param current_code_matrix: Conversion rule between base and binary data based on support base and current base (RULE 2).
                                     Label row is the support base, label col is the current base.
                                         B1  B2  B3  B4
                                     B1  X1  Y1  X2  Y2
                                     B2  X3  Y3  X4  Y4
                                     B3  X5  Y5  X6  Y6
                                     B4  X7  Y7  X8  Y8
                                     Where B1 and B2 correspond to two bases with the same value, B3 and B4 are the same rule as B1 and B2.
                                     Make sure that Xn + Yn = 1 and Xn * Yn = 0, n is in [1, 8].

        :param support_bases: Base replenishment before official data.
                               Make sure that the count of support base must more than support spacing.
                               Make sure that the number range of each position is {0, 1, 2, 3}, reference base index.

        :param support_spacing: Spacing between support base and current base.
                                 When the support base is the front of the current base, the spacing is 0.

        :param max_ratio: The max ratio of 0 or 1.
                           When the (count/length) >= this parameter, we decide that this binary sequence is not good.

        """
        log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                   "Create the DDC method.")

        # check support bases
        for index in range(len(support_bases)):
            if support_bases[index] != 'A' and support_bases[index] != 'T' and support_bases[index] != 'C' and support_bases[index] != 'G':
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "Only A, T, C, and G can be included in the support bases, "
                           "and the support bases[" + str(index) + "] has entered " + str(support_bases[index] + "!"))
        if len(support_bases) < support_spacing + 1:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "The count of support base needs more than support spacing!")

        # check base reference (rule 1)
        for index in range(len(base_reference)):
            if base_reference[index] != 0 and base_reference[index] != 1:
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "Only 0 and 1 can be included in the base reference, "
                           "and your number " + str(index) + " has entered " + str(base_reference[index] + "!"))
        if sum(base_reference) != 2:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "Wrong correspondence between base and binary data!")

        # check current code matrix (rule 2)
        for row in range(len(current_code_matrix)):
            for col in range(len(current_code_matrix[row])):
                if current_code_matrix[row][col] != 0 and current_code_matrix[row][col] != 1:
                    log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                               "Only 0 and 1 can be included in the current code matrix, "
                               "and the current code matrix [" + str(index) + "] has entered " + str(base_reference[index] + "!"))
        for row in range(len(current_code_matrix)):
            if base_reference[0] == base_reference[1]:
                for col in range(0, len(current_code_matrix[row]) - 1, 2):
                    if current_code_matrix[row][col] + current_code_matrix[row][col + 1] == 1 and current_code_matrix[row][col] * current_code_matrix[row][col + 1] == 0:
                        continue
                    else:
                        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                                   "Wrong current code matrix, "
                                   "the error locations are [" + str(row) + ", " + str(col) + "] and [" + str(row) + ", " + str(col) + "]! "
                                   "Rules are that they add up to 1 and multiply by 0.")
            elif base_reference[0] == base_reference[2]:
                for col in range(len(current_code_matrix[row]) - 2):
                    if current_code_matrix[row][col] + current_code_matrix[row][col + 2] == 1 and current_code_matrix[row][col] * current_code_matrix[row][col + 2] == 0:
                        continue
                    else:
                        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                                   "Wrong current code matrix, "
                                   "the error locations are [" + str(row) + ", " + str(col) + "] and [" + str(row) + ", " + str(col) + "]! "
                                   "Rules are that they add up to 1 and multiply by 0.")

            else:
                for col in range(len(current_code_matrix[row]) - 3):
                    if current_code_matrix[row][col] + current_code_matrix[row][col + 3] == 1 and current_code_matrix[row][col] * current_code_matrix[row][col + 3] == 0:
                        continue
                    else:
                        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                                   "Wrong current code matrix, "
                                   "the error locations are [" + str(row) + ", " + str(col) + "] and [" + str(row) + ", " + str(col) + "]! "
                                   "Rules are that they add up to 1 and multiply by 0.")
        # check max ratio
        if max_ratio <= 0.5 or max_ratio >= 1:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "Wrong max ratio (" + str(max_ratio) + ")!")
