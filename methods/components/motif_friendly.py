"""
Name: Friendly Check Function

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) Determine whether motif is friendly to sequencing and synthesis by multiple indicators.
"""

import sys

from utils import log


# noinspection PyProtectedMember
def friendly_check(dna_motif, base_index=None, max_repeat=6, max_content=0.8):
    """
    introduction: Check DNA motif for friendliness.

    :param dna_motif: DNA motif for detection.
                       Type: string.

    :param base_index: The relationship between base and index can be derived from the corresponding coding method.

    :param max_repeat: Maximum repetition times of single base repetition.
                        Make sure that this parameter must more than zero.

    :param max_content: Maximum content of C/G or A/T.
                         Make sure that this parameter should belong to the open range of 0 to 1.

    :return: friendly: If one of the conditions is not satisfied, we conclude that this DNA motif is unfriendly.
    """

    if len(dna_motif) < max_repeat:
        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                   "The maximum number of repeats in the single base should not be longer than the length of the DNA motif.")

    if max_repeat < 0:
        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                   "The value of max_repeat should more than 0.")

    if max_content < 0.5 or max_content >= 1:
        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                   "The value of max content should belong to the open range of 0 to 1.")

    if max(repeat_single_base(dna_motif, base_index)) >= max_repeat:
        # print("\n" + ''.join(dna_motif))
        # print(repeat_single_base(dna_motif, base_index))
        return False

    if cg_content(dna_motif) < (1 - max_content) or cg_content(dna_motif) > max_content:
        return False

    if min_free_energy(dna_motif) > -30:
        return False

    return True


def repeat_single_base(dna_motif, base_index=None):

    if not base_index:
        base_index = {'A': 0, 'T': 1, 'C': 2, 'G': 3}

    counts = [0, 0, 0, 0]
    last_base = None
    save_base = None
    current_count = 1

    for index in range(len(dna_motif)):
        if last_base is not None:
            if dna_motif[index] != last_base:
                if counts[base_index[save_base]] < current_count:
                    counts[base_index[save_base]] = current_count
                    current_count = 1
                last_base = dna_motif[index]
                save_base = last_base
            else:
                if index == len(dna_motif) - 1:
                    if counts[base_index[save_base]] < current_count:
                        counts[base_index[save_base]] = current_count
                else:
                    current_count += 1

        else:
            last_base = dna_motif[index]
            save_base = last_base

    return counts


def cg_content(dna_motif):

    count = 0

    for index in range(len(dna_motif)):
        if dna_motif[index] == 'C' or dna_motif[index] == 'G':
            count += 1

    return count / len(dna_motif)


def min_free_energy(dna_motif):
    # TODO It could be used the framework: rnafold.
    return -30
