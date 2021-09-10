import os
import Chamaeleo
from Chamaeleo.methods.default import BaseCodingAlgorithm
from Chamaeleo.methods.ecc import Hamming, ReedSolomon
from Chamaeleo.methods.fixed import Church, Goldman, Grass, Blawat
from Chamaeleo.methods.flowed import DNAFountain, YinYangCode
from Chamaeleo.utils.pipelines import TranscodePipeline


if __name__ == "__main__":
    root_path = os.path.dirname(Chamaeleo.__file__)
    current_path = os.path.dirname(os.path.realpath(__file__))
    generated_file_path = os.path.join(current_path, "generated_files")

    read_file_path = os.path.join(root_path, "data", "pictures", "Mona Lisa.jpg")
    write_file_path = os.path.join(generated_file_path, "target.jpg")
    dna_path = os.path.join(generated_file_path, "target.dna")

    coding_schemes = {
        "Base": BaseCodingAlgorithm(),
        "Church et al.": Church(), "Goldman et al.": Goldman(), "Grass et al.": Grass(), "Blawat et al.": Blawat(),
        "DNA Fountain": DNAFountain(), "Yin-Yang Code": YinYangCode()
    }

    error_corrections = {
        "None": None, "Hamming": Hamming(), "ReedSolomon": ReedSolomon()
    }

    needed_indices = [
        True,
        True, True, True, True,
        False, True
    ]

    for (scheme_name, coding_scheme), needed_index in zip(coding_schemes.items(), needed_indices):
        for code_name, error_correction in error_corrections.items():
            print(">" * 50)
            print("*" * 50)
            if error_correction is not None:
                print("Doing coding scheme [" + scheme_name + "] with error correction [" + code_name + "].")
            else:
                print("Doing coding scheme [" + scheme_name + "].")
            print("*" * 50)

            pipeline = TranscodePipeline(coding_scheme=coding_scheme, error_correction=error_correction, need_logs=True)

            try:
                encoded_data = pipeline.transcode(direction="t_c", input_path=read_file_path, output_path=dna_path,
                                                  segment_length=120, index=needed_index)

                decoded_data = pipeline.transcode(direction="t_s", input_path=dna_path, output_path=write_file_path,
                                                  index=needed_index)

                print()
                pipeline.output_records(type="string")
                print("transcoding state: " + str(encoded_data["bit"] == decoded_data["bit"]))
                print()

            except ValueError as error:
                print(error)
