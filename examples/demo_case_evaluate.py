import os
import Chamaeleo

from Chamaeleo.methods.default import BaseCodingAlgorithm
from Chamaeleo.methods.ecc import Hamming, ReedSolomon
from Chamaeleo.methods.fixed import Church, Goldman, Grass, Blawat
from Chamaeleo.methods.flowed import DNAFountain, YinYangCode
from Chamaeleo.utils.pipelines import EvaluatePipeline


if __name__ == "__main__":
    root_path = os.path.dirname(Chamaeleo.__file__)

    file_paths = {
        "Mona Lisa.jpg": os.path.join(root_path, "data", "pictures", "Mona Lisa.jpg"),
        "Microsoft Winmine.exe": os.path.join(root_path, "data", "binaries", "Microsoft Winmine.exe")
    }

    coding_schemes = {
        "Base": BaseCodingAlgorithm(),
        "Church et al.": Church(), "Goldman et al.": Goldman(), "Grass et al.": Grass(), "Blawat et al.": Blawat(),
        "DNA Fountain": DNAFountain(),
        "Yin-Yang Code": YinYangCode()
    }
    error_corrections = {
        "None": None,
        "Hamming": Hamming(),
        "ReedSolomon": ReedSolomon()
    }

    needed_indices = [
        True,
        True, True, True, True,
        False,
        True
    ]

    pipeline = EvaluatePipeline(
        coding_schemes=coding_schemes,
        error_corrections=error_corrections,
        needed_indices=needed_indices,
        file_paths=file_paths,
        nucleotide_insertion=0.001,
        nucleotide_mutation=0.001,
        nucleotide_deletion=0.001,
        sequence_loss=0.001,
        iterations=3,
        segment_length=120,
        need_logs=True
    )

    pipeline.evaluate()
    pipeline.output_records(type="string")
