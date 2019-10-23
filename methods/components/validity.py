"""
Name: Validity

Coder: HaoLing ZHANG (BGI-Research)[V1]

Function(s):
Check the validity of requested DNA sequence.
The validity describes the friendly index for DNA synthesis, sequencing and related operations
"""


def check(sequence, max_homopolymer=4, max_simple_segment=6, max_content=0.6):
    """
    Check the validity of requested DNA sequence.

    :param sequence: requested DNA sequence.
    :param max_homopolymer: maximum length of homopolymer.
    :param max_simple_segment: maximum length of simple segment, including (normal, inverse, dyad) motif repeat.
    :param max_content: maximum content of C and G, which means GC content is in [1 - max_content, max_content].

    :return: whether the DNA sequence is validly.
    """
    if not homopolymer(sequence, max_homopolymer):
        return False
    if not motif_repeat(sequence, max_simple_segment):
        return False
    if not dyad_motif_repeat(sequence, max_simple_segment):
        return False
    if not inverse_motif_repeat(sequence, max_simple_segment):
        return False
    if not cg_content(sequence, max_content):
        return False

    return True


def homopolymer(sequence, max_homopolymer):
    """
    Check the max homopolymer of requested DNA sequence.

    :param sequence: DNA sequence needs detecting.
    :param max_homopolymer: aximum length of homopolymer.

    :return: whether the DNA sequence is validly.
    """
    base_index = {'A': 0, 'T': 1, 'C': 2, 'G': 3}
    counts = [0, 0, 0, 0]
    last_base = None
    save_base = None
    current_count = 1

    for index in range(len(sequence)):
        if last_base is not None:
            if sequence[index] != last_base:
                if counts[base_index[save_base]] < current_count:
                    counts[base_index[save_base]] = current_count
                current_count = 1
                last_base = sequence[index]
                save_base = last_base
            else:
                if index == len(sequence) - 1:
                    if counts[base_index[save_base]] < current_count:
                        counts[base_index[save_base]] = current_count
                else:
                    current_count += 1

        else:
            last_base = sequence[index]
            save_base = last_base

    return max(counts) <= max_homopolymer


def motif_repeat(sequence, max_length):
    """
    Check the motif repeat of requested DNA sequence.

    :param sequence: requested DNA sequence.
    :param max_length: maximum length of simple segment, including (normal, inverse, dyad) motif repeat.

    :return: whether the DNA sequence is validly.
    """
    length = len(sequence) - 1
    while length > max_length:
        for index in range(len(sequence)):
            if index + length < len(sequence):
                sample = sequence[index: index + length]
                if sequence.count(sample) > 1:
                    return False
        length -= 1

    return True


def inverse_motif_repeat(sequence, max_length):
    """
    Check the inverse motif repeat of requested DNA sequence.

    :param sequence: requested DNA sequence.
    :param max_length: maximum length of simple segment, including (normal, inverse, dyad) motif repeat.

    :return: whether the DNA sequence is validly.
    """
    length = len(sequence) - 1
    while length > max_length:
        for index in range(len(sequence)):
            if index + length < len(sequence):
                sample = sequence[index: index + length]
                if sequence.count(sample[::-1]) > 0:
                    return False
        length -= 1

    return True


def dyad_motif_repeat(sequence, max_length):
    """
    Check the dyad motif repeat of requested DNA sequence.

    :param sequence: requested DNA sequence.
    :param max_length: maximum length of simple segment, including (normal, inverse, dyad) motif repeat.

    :return: whether the DNA sequence is validly.
    """
    length = len(sequence) - 1
    dyad_motif = ""
    for index in range(len(sequence)):
        if sequence[index] == "A":
            dyad_motif += "T"
        elif sequence[index] == "T":
            dyad_motif += "A"
        elif sequence[index] == "C":
            dyad_motif += "G"
        else:
            dyad_motif += "C"

    while length > max_length:
        for index in range(len(sequence)):
            if index + length < len(sequence):
                sample = sequence[index: index + length]
                if dyad_motif.count(sample[::-1]) > 0:
                    return False
        length -= 1

    return True


def cg_content(motif, max_content):
    """
    Check the C and G content of requested DNA sequence.

    :param motif: requested DNA sequence.
    :param max_content: maximum content of C and G, which means GC content is in [1 - max_content, max_content].

    :return: whether the DNA sequence is validly.
    """
    return (1 - max_content) <= float(motif.count("C") + motif.count("G")) / float(len(motif)) <= max_content
