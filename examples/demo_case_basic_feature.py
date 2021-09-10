import os
import Chamaeleo
from Chamaeleo.methods.default import BaseCodingAlgorithm
from Chamaeleo.methods.fixed import Church, Goldman, Grass, Blawat
from Chamaeleo.methods.flowed import DNAFountain, YinYangCode
from Chamaeleo.utils.pipelines import BasicFeaturePipeline


if __name__ == "__main__":
    root_path = os.path.dirname(Chamaeleo.__file__)

    file_paths = {
        "Mona Lisa.jpg": os.path.join(root_path, "data", "pictures", "Mona Lisa.jpg")
    }

    coding_schemes = {
        "Base": BaseCodingAlgorithm(),
        "Church et al.": Church(), "Goldman et al.": Goldman(), "Grass et al.": Grass(), "Blawat et al.": Blawat(),
        "DNA Fountain": DNAFountain(redundancy=0.5), "Yin-Yang Code": YinYangCode()
    }
    needed_indices = [
        True,
        True, True, True, True,
        False, True
    ]

    pipeline = BasicFeaturePipeline(
        coding_schemes=coding_schemes,
        needed_indices=needed_indices,
        file_paths=file_paths,
        segment_length=128,
        index_length=16,
        need_logs=True)

    pipeline.calculate()
    pipeline.output_records(type="string")
