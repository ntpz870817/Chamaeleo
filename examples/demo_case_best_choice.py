import os
import Chamaeleo

from Chamaeleo.methods.default import BaseCodingAlgorithm
from Chamaeleo.methods.fixed import Church

from Chamaeleo.utils.pipelines import OptimalChoicePipeline

if __name__ == "__main__":
    root_path = os.path.dirname(Chamaeleo.__file__)
    read_file_path = os.path.join(root_path, "data", "pictures", "Mona Lisa.jpg")

    current_path = os.path.dirname(os.path.realpath(__file__))
    generated_file_path = os.path.join(current_path, "generated_files")
    dna_path = os.path.join(generated_file_path, "target.dna")

    feature_log_path = os.path.join(root_path, "examples", "log_files", "seq_features.logs")
    robustness_log_path = os.path.join(root_path, "examples", "log_files", "robustness.logs")

    coding_schemes = {
        "Base": BaseCodingAlgorithm(), "Church et al.": Church()
    }

    pipeline = OptimalChoicePipeline(
        coding_schemes=coding_schemes,
        feature_log_path=feature_log_path,
        robustness_log_path=robustness_log_path
    )

    pipeline.calculate_best()

    pipeline.output_records(
        selected_coding_scheme="Church et al.",
        error_correction=None,
        input_path=read_file_path, output_path=dna_path,
        segment_length=256, needed_index=True, need_logs=True,
    )
