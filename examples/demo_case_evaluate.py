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
        "DNA Fountain Input Files.tar": os.path.join(root_path, "data", "binaries", "DNA Fountain Input Files.tar"),
        "Microsoft Winmine.exe": os.path.join(root_path, "data", "binaries", "Microsoft Winmine.exe"),
        "A Tale of Two Cities.pdf": os.path.join(root_path, "data", "books", "A Tale of Two Cities.pdf"),
        "The Wandering Earth.pdf": os.path.join(root_path, "data", "books", "The Wandering Earth.pdf"),
        "For Elise.wma": os.path.join(root_path, "data", "musics", "For Elise.wma"),
        "Summer.mp3": os.path.join(root_path, "data", "musics", "Summer.mp3"),
        "Mona Lisa.jpg": os.path.join(root_path, "data", "pictures", "Mona Lisa.jpg"),
        "United Nations Flag.bmp": os.path.join(root_path, "data", "pictures", "United Nations Flag.bmp"),
        "Exiting the Factory.flv": os.path.join(root_path, "data", "videos", "Exiting the Factory.flv"),
        "I have a Dream.mp4": os.path.join(root_path, "data", "videos", "I have a Dream.mp4")
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
        iterations=2,
        segment_length=120,
        need_tips=True
    )

    pipeline.evaluate()
    pipeline.output_logs(type="string")
