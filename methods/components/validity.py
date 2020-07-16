"""
Name: Validity

Coder: HaoLing ZHANG (BGI-Research)[V1]

Function(s):
Check the validity of requested DNA sequence.
The validity describes the friendly index for DNA synthesis, sequencing and related operations
"""


def check(sequence, max_homopolymer=4,  max_content=0.6):
    """
    Check the validity of requested DNA sequence.

    :param sequence: requested DNA sequence.
    :param max_homopolymer: maximum length of homopolymer.
    :param max_content: maximum content of C and G, which means GC content is in [1 - max_content, max_content].

    :return: whether the DNA sequence can be considered as valid for DNA synthesis and sequencing.
    """
    if not homopolymer(sequence, max_homopolymer):
        return False
    if not cg_content(sequence, max_content):
        return False

    return True


def homopolymer(sequence, max_homopolymer):
    """
    Check the max homopolymer of requested DNA sequence.

    :param sequence: DNA sequence needs detecting.
    :param max_homopolymer: maximum length of homopolymer.

    :return: whether the DNA sequence can be considered as valid for DNA synthesis and sequencing.
    """
    missing_segments = [
        "A" * (1 + max_homopolymer),
        "C" * (1 + max_homopolymer),
        "G" * (1 + max_homopolymer),
        "T" * (1 + max_homopolymer)]
    for missing_segment in missing_segments:
        if missing_segment in "".join(sequence):
            return False
    return True


def cg_content(motif, max_content):
    """
    Check the C and G content of requested DNA sequence.

    :param motif: requested DNA sequence.
    :param max_content: maximum content of C and G, which means GC content is in [1 - max_content, max_content].

    :return: whether the DNA sequence can be considered as valid for DNA synthesis and sequencing.
    """
    return (1 - max_content) <= float(motif.count("C") + motif.count("G")) / float(len(motif)) <= max_content
