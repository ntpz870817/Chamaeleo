def check(dna_motif, max_base_repeat=4, max_motif_repeat=3, max_content=0.6):
    """

    :param dna_motif:
    :param max_base_repeat:
    :param max_motif_repeat:
    :param max_content:
    :return:
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

    return True


def base_repeat(dna_motif, max_repeat):
    """

    :param dna_motif:
    :param max_repeat:
    :return:
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

    :param dna_motif:
    :param max_repeat:
    :return:
    """
    length = len(dna_motif) - 1
    while length > max_repeat:
        for index in range(len(dna_motif)):
            if index + length < len(dna_motif):
                sample = dna_motif[index: index + length]
                if dna_motif.count(str(sample)) > 1:
                    return False
        length -= 1

    return True


def inverse_motif_repeat(motif, max_repeat):
    """

    :param motif:
    :param max_repeat:
    :return:
    """
    length = len(motif) - 1
    while length > max_repeat:
        for index in range(len(motif)):
            if index + length < len(motif):
                sample = motif[index: index + length]
                if motif.count(str(sample[::-1])) > 0:
                    return False
        length -= 1

    return True


def dyad_motif_repeat(motif, max_repeat):
    """

    :param motif:
    :param max_repeat:
    :return:
    """
    length = len(motif) - 1
    dyad_motif = ""
    for index in range(len(motif)):
        if motif[index] == "A":
            dyad_motif += "T"
        elif motif[index] == "T":
            dyad_motif += "A"
        elif motif[index] == "C":
            dyad_motif += "G"
        else:
            dyad_motif += "C"

    while length > max_repeat:
        for index in range(len(motif)):
            if index + length < len(motif):
                sample = motif[index: index + length]
                if dyad_motif.count(str(sample[::-1])) > 0:
                    return False
        length -= 1

    return True


def cg_content(motif, max_content):
    """

    :param motif:
    :param max_content:
    :return:
    """
    return (1 - max_content) <= float(motif.count("C") + motif.count("G")) / float(len(motif)) <= max_content
