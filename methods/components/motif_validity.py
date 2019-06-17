"""
Name: Friendly Check

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1.1

Function(s): (1) Determine whether motif is friendly to sequencing and synthesis by multiple indicators.
"""

import sys

from utils import log


def friendly_check(dna_motif, max_base_repeat=6, max_motif_repeat=4, max_content=0.8, min_free_energy_value=-30):
    """
    introduction: Check DNA motif for friendliness.

    :param dna_motif: DNA motif for detection.
                       Type: string.

    :param max_base_repeat: The relationship between base and index can be derived from the corresponding coding method.

    :param max_motif_repeat: Maximum repetition times of single base repetition.
                               Make sure that this parameter must more than zero.

    :param max_content: Maximum content of C/G or A/T.
                         Make sure that this parameter should belong to the open range of 0 to 1.

    :param min_free_energy_value: The value of minimum free energy.

    :return: If one of the conditions is not satisfied, we conclude that this DNA motif is unfriendly.
    """
    if base_repeat(dna_motif, max_base_repeat) is False:
        return False
    if motif_repeat(dna_motif, max_motif_repeat) is False:
        return False
    if dyad_motif_repeat(dna_motif, max_motif_repeat) is False:
        return False
    if inverse_motif_repeat(dna_motif, max_motif_repeat) is False:
        return False
    if cg_content(dna_motif, max_content) is False:
        return False
    if min_free_energy(dna_motif, min_free_energy_value) is False:
        return False

    return True


def base_repeat(dna_motif, max_repeat):
    """
    introduction: Compute the continuous single base repetition in a DNA motif.

    :param dna_motif: DNA motif for detection.
                       Type: string.

    :param max_repeat: Maximum repetition times.
                        More than that time, the DNA motif was considered unfriendly.

    :return: Whether DNA motif conforms to the friendliness or not.
    """
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

    return max(counts) <= max_repeat


def motif_repeat(dna_motif, max_repeat):
    """
    introduction: Compute the continuous repetition of fragments in a DNA motif.

    :param dna_motif:  DNA motif for detection.
                       Type: string.

    :param max_repeat: Maximum repetition times.
                        More than that time, the DNA motif was considered unfriendly.

    :return: Whether DNA motif conforms to the friendliness or not.
    """
    length = len(dna_motif) - 1
    while length > max_repeat:
        for index in range(len(dna_motif)):
            if index + length < len(dna_motif):
                sample = dna_motif[index: index + length]
                if dna_motif.count(sample) > 1:
                    return False
        length -= 1

    return True


def inverse_motif_repeat(dna_motif, max_repeat):
    """
    introduction: Compute the inverse repetition of fragments in a DNA motif.

    :param dna_motif: DNA motif for detection.
                       Type: string.

    :param max_repeat: Maximum repetition times.
                        More than that time, the DNA motif was considered unfriendly.

    :return: Whether DNA motif conforms to the friendliness or not.
    """
    length = len(dna_motif) - 1
    while length > max_repeat:
        for index in range(0, len(dna_motif) - 2 * length):
            sample = dna_motif[index: index + length]
            inverse_sample = sample[::-1]
            if dna_motif.count(inverse_sample) > 0:
                return False
        length -= 1

    return True


def dyad_motif_repeat(dna_motif, max_repeat):
    """
    introduction: Compute the complementary repetition of fragments in a DNA motif.

    :param dna_motif: DNA motif for detection.
                       Type: string.

    :param max_repeat: Maximum repetition times.
                        More than that time, the DNA motif was considered unfriendly.

    :return: Whether DNA motif conforms to the friendliness or not.
    """
    length = len(dna_motif) - 1
    while length > max_repeat:
        for index in range(len(dna_motif)):
            if index + length < len(dna_motif):
                sample = dna_motif[index: index + length]
                if dna_motif.count(sample[::-1]) > 0:
                    return False
        length -= 1

    return True


def cg_content(dna_motif, max_content):
    """
    introduction: Compute the complementary repetition of fragments in a DNA motif.

    :param dna_motif: DNA motif for detection.
                       Type: string.

    :param max_content: CG or AT Maximum repetition content.
                         More than that content, the DNA motif was considered unfriendly.

    :return: Whether DNA motif conforms to the friendliness or not.
    """
    return (1 - max_content) < float(dna_motif.count("C") + dna_motif.count("G")) / len(dna_motif) < max_content


# noinspection PyUnusedLocal
def min_free_energy(dna_motif, min_free_energy_value):
    """
    introduction: Compute the continuous repetition of fragments in a DNA motif.

    :param dna_motif:  DNA motif for detection.
                       Type: string.

    :param min_free_energy_value: Min free energy value.
                                   More than that value, the DNA motif was considered unfriendly.

    :return: Whether DNA motif conforms to the friendliness or not.
    """
    # TODO It could be used the framework: rnafold.
    return True
