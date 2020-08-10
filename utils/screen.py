def check(sequence, max_homopolymer=4, max_content=0.6):
    if not homopolymer(sequence, max_homopolymer):
        return False
    if not gc_content(sequence, max_content):
        return False

    return True


def homopolymer(sequence, max_homopolymer):
    missing_segments = [
        "A" * (1 + max_homopolymer),
        "C" * (1 + max_homopolymer),
        "G" * (1 + max_homopolymer),
        "T" * (1 + max_homopolymer)]
    for missing_segment in missing_segments:
        if missing_segment in "".join(sequence):
            return False
    return True


def gc_content(motif, max_content):
    return (1 - max_content) <= (float(motif.count("C") + motif.count("G")) / float(len(motif))) <= max_content
