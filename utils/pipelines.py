import copy
import os
import random

from Chamaeleo.methods.default import AbstractCodingAlgorithm, AbstractErrorCorrectionCode
from Chamaeleo.utils import data_handle, indexer
from Chamaeleo.utils.monitor import Monitor


class DefaultPipeline(object):

    def __init__(self, **info):
        self.need_logs = info["need_logs"] if "need_logs" in info else False
        self.monitor = Monitor()
        self.records = {}

    def __init_check__(self):
        if type(self.need_logs) != bool:
            raise ValueError("\"need_logs\" must be bool type!")

    def output_records(self, **info):
        raise NotImplementedError("\"output_records\" interface needs to be implemented!")


class TranscodePipeline(DefaultPipeline):

    def __init__(self, **info):
        super().__init__(**info)
        self.coding_scheme = info["coding_scheme"] if "coding_scheme" in info else None
        self.error_correction = info["error_correction"] if "error_correction" in info else None

        self.__init_check__()

        if self.need_logs:
            print("Create a transcoding pipeline.")
            self.coding_scheme.need_logs = True
            if self.error_correction is not None:
                self.error_correction.need_logs = True

    def __init_check__(self):
        super().__init_check__()
        if self.coding_scheme is None:
            raise ValueError("No coding scheme!")

        if not isinstance(self.coding_scheme, AbstractCodingAlgorithm):
            raise ValueError("The \"coding_scheme\" needs to "
                             + "inherit AbstractCodingScheme in methods/pipelines.py!")

        if self.error_correction is not None and not isinstance(self.error_correction, AbstractErrorCorrectionCode):
            raise ValueError("The error correction needs to "
                             + "inherit AbstractErrorCorrectionCode in methods/pipelines.py!")

    def transcode(self, **info):
        if "direction" in info:
            if info["direction"] == "t_c":
                segment_length = info["segment_length"] if "segment_length" in info else 120

                self.records["payload length"] = segment_length

                if "input_path" in info:
                    bit_segments, bit_size = data_handle.read_bits_from_file(info["input_path"], segment_length,
                                                                             self.need_logs)
                elif "input_string" in info:
                    bit_segments, bit_size = data_handle.read_bits_from_str(info["input_string"], segment_length,
                                                                            self.need_logs)
                else:
                    raise ValueError("There is no digital data input here!")

                original_bit_segments = copy.deepcopy(bit_segments)

                if "index" in info and info["index"]:
                    bit_segments, index_length = indexer.connect_all(bit_segments, self.need_logs)
                    self.records["index length"] = index_length
                else:
                    self.records["index length"] = 0

                if self.error_correction is not None:
                    bit_segments, error_correction_length = self.error_correction.insert(bit_segments)
                    self.records["error-correction length"] = error_correction_length
                else:
                    self.records["error-correction length"] = 0

                results = self.coding_scheme.silicon_to_carbon(bit_segments, bit_size)

                dna_sequences = results["dna"]

                self.records["information density"] = round(results["i"], 3)
                self.records["encoding runtime"] = round(results["t"], 3)

                if "output_path" in info:
                    data_handle.write_dna_file(info["output_path"], dna_sequences, self.need_logs)

                return {"bit": original_bit_segments, "dna": dna_sequences}
            elif info["direction"] == "t_s":
                if "input_path" in info:
                    dna_sequences = data_handle.read_dna_file(info["input_path"], self.need_logs)
                elif "input_string" in info:
                    dna_sequences = []
                    for index, string in enumerate(info["input_string"]):
                        dna_sequences.append(string)
                else:
                    raise ValueError("There is no digital data input here!")

                original_dna_sequences = copy.deepcopy(dna_sequences)

                results = self.coding_scheme.carbon_to_silicon(dna_sequences)
                self.records["decoding runtime"] = round(results["t"], 3)

                bit_segments = results["bit"]
                bit_size = results["s"]

                if not bit_segments:
                    self.records["error rate"] = "100.00%"
                    return {"bit": None, "dna": original_dna_sequences}

                if self.error_correction is not None:
                    verified_data = self.error_correction.remove(bit_segments)
                    bit_segments = verified_data["bit"]
                    self.records["error rate"] = str(round(verified_data["e_r"] * 100, 2)) + "%"
                    self.records["error indices"] = verified_data["e_i"] if verified_data["e_i"] != [] else None
                    self.records["error bit segments"] = verified_data["e_bit"] if verified_data["e_bit"] != [] else None
                else:
                    self.records["error rate"] = None
                    self.records["error indices"] = None
                    self.records["error bit segments"] = None

                if not bit_segments:
                    return {"bit": None, "dna": original_dna_sequences}

                if "index" in info and info["index"]:
                    indices, bit_segments = indexer.divide_all(bit_segments, self.need_logs)
                    bit_segments = indexer.sort_order(indices, bit_segments, self.need_logs)

                if "output_path" in info:
                    data_handle.write_bits_to_file(info["output_path"], bit_segments, bit_size, self.need_logs)
                elif "output_string" in info:
                    string = data_handle.write_bits_to_str(bit_segments, bit_size, self.need_logs)
                    if self.need_logs:
                        print(string)

                return {"bit": bit_segments, "dna": original_dna_sequences}
            else:
                raise ValueError("Unknown parameter \"direction\", please use \"t_c\" or \"t_s\".")
        else:
            raise ValueError("Unknown parameter \"direction\", please use \"t_c\" or \"t_s\".")

    def output_records(self, **info):
        if "type" in info:
            if info["type"] == "path":
                if "path" in info:
                    with open(info["path"], "w", encoding="utf-8") as save_file:
                        for key, value in self.records.items():
                            if type(value) == str:
                                save_file.write(key + "," + value + "\n")
                            else:
                                save_file.write(key + "," + str(value) + "\n")
                else:
                    raise ValueError("\"path\" is unknown!")
            elif info["type"] == "string":
                if self.need_logs:
                    print("Transcoding log: ")
                    for key, value in self.records.items():
                        if type(value) == str:
                            print(key + ": " + value)
                        else:
                            print(key + ": " + str(value))

        return self.records


class EvaluatePipeline(DefaultPipeline):

    def __init__(self, **info):
        super().__init__(**info)

        self.coding_schemes = info["coding_schemes"] if "coding_schemes" in info else None
        self.error_corrections = info["error_corrections"] if "error_corrections" in info else None

        self.needed_indices = info["needed_indices"] if "needed_indices" in info else None

        self.file_paths = info["file_paths"] if "file_paths" in info else None

        self.nucleotide_insertion = info["nucleotide_insertion"] if "nucleotide_insertion" in info else 0
        self.nucleotide_mutation = info["nucleotide_mutation"] if "nucleotide_mutation" in info else 0
        self.nucleotide_deletion = info["nucleotide_deletion"] if "nucleotide_deletion" in info else 0
        self.sequence_loss = info["sequence_loss"] if "sequence_loss" in info else 0
        self.iterations = info["iterations"] if "iterations" in info else 1

        self.segment_length = info["segment_length"] if "segment_length" in info else 120

        self.__init_check__()

        self.records = {
            "evaluation parameters": {
                "evaluated coding schemes": list(self.coding_schemes.keys()),
                "evaluated files": list(self.file_paths.keys()),
                "evaluated error correction": list(self.error_corrections.keys()),
                "original segment length": self.segment_length,
                "perturbation": {
                    "nucleotide insertion": self.nucleotide_insertion,
                    "nucleotide mutation": self.nucleotide_mutation,
                    "nucleotide deletion": self.nucleotide_deletion,
                    "sequence loss": self.sequence_loss,
                    "iterations": self.iterations
                }
            }
        }

    def __init_check__(self):
        super().__init_check__()
        if self.coding_schemes is None:
            raise ValueError("No coding scheme!")
        for name, coding_scheme in self.coding_schemes.items():
            if not isinstance(coding_scheme, AbstractCodingAlgorithm):
                raise ValueError("\"coding_scheme \" " + str(name) + "[" + str(type(coding_scheme))
                                 + "] needs to inherit AbstractCodingScheme in methods/pipelines.py!")

        if self.error_corrections is None:
            raise ValueError("No error correction!")
        for name, error_correction in self.error_corrections.items():
            if error_correction is not None and not isinstance(error_correction, AbstractErrorCorrectionCode):
                raise ValueError("\"error_correction \" " + str(name) + "[" + str(type(error_correction))
                                 + "] needs to inherit AbstractErrorCorrectionCode in methods/pipelines.py!")

        if self.needed_indices is None:
            raise ValueError("Whether each coding scheme needs \"index\" needs to be explained!")
        if len(self.coding_schemes) != len(self.needed_indices):
            raise ValueError("Coding scheme and its index requirements need to be matched one by one!")
        for index, needed_index in enumerate(self.needed_indices):
            if type(needed_index) is not bool:
                raise ValueError(str(index) in "\"needed_indices\" must be bool type!")

        if self.file_paths is None:
            raise ValueError("No digital file path!")
        for file_name, file_path in self.file_paths.items():
            if not os.path.exists(file_path):
                raise ValueError("The path of digital file " + str(file_name) + ": " + file_path + " does not exist!")

        if self.nucleotide_insertion > 1 or self.nucleotide_insertion < 0:
            raise ValueError("Wrong value in the \"nucleotide_insertion\", the value is in the range of [0, 1]!")
        if self.nucleotide_mutation > 1 or self.nucleotide_mutation < 0:
            raise ValueError("Wrong value in the \"nucleotide_mutation\", the value is in the range of [0, 1]!")
        if self.nucleotide_deletion > 1 or self.nucleotide_deletion < 0:
            raise ValueError("Wrong value in the \"nucleotide_deletion\", the value is in the range of [0, 1]!")
        if self.sequence_loss > 1 or self.sequence_loss < 0:
            raise ValueError("Wrong value in the \"sequence_loss\", the value is in the range of [0, 1]!")

        if self.segment_length <= -1 or type(self.segment_length) != int:
            raise ValueError("Wrong value in the \"segment_length\", "
                             "the value is in the range of [-1, +inf) and the type is int!")

        if self.iterations < 1 or type(self.iterations) != int:
            raise ValueError("Wrong value in the \"iterations\", "
                             "the value is in the range of [1, +inf) and the type is int!")

    def evaluate(self):
        results = {}
        task_index = 0
        total_task = len(self.coding_schemes) * len(self.error_corrections) * len(self.file_paths)
        for (scheme_name, coding_scheme), needed_index in zip(self.coding_schemes.items(), self.needed_indices):
            for correct_name, error_correction in self.error_corrections.items():
                for file_name, file_path in self.file_paths.items():
                    if self.need_logs:
                        print(">" * 50)
                        print("*" * 50)
                        print("Run task (" + str(task_index + 1) + "/" + str(total_task) + ").")
                        print("*" * 50)

                    pipeline = TranscodePipeline(coding_scheme=coding_scheme, error_correction=error_correction,
                                                 need_logs=self.need_logs)

                    encoded_data = pipeline.transcode(direction="t_c", input_path=file_path,
                                                      segment_length=self.segment_length, index=needed_index)

                    pipeline_logs = []
                    for iteration in range(self.iterations):
                        # print("iteration " + str(iteration + 1) + ": ")
                        chosen_count = int(len(encoded_data["dna"]) * (1 - self.sequence_loss))
                        dna_sequences = random.sample(copy.deepcopy(encoded_data["dna"]), chosen_count)

                        total_indices = [sequence_index for sequence_index in range(len(dna_sequences))]

                        # insertion errors
                        for insertion_iteration in range(int(len(dna_sequences) * self.nucleotide_insertion)):
                            chosen_index = random.choice(total_indices)
                            dna_sequences[chosen_index].insert(random.randint(0, len(dna_sequences[chosen_index]) - 1),
                                                               random.choice(['A', 'C', 'G', 'T']))

                        # mutation errors
                        for mutation_iteration in range(int(len(dna_sequences) * self.nucleotide_mutation)):
                            chosen_index = random.choice(total_indices)
                            chosen_index_in_sequence = random.randint(0, len(dna_sequences[chosen_index]) - 1)
                            chosen_nucleotide = dna_sequences[chosen_index][chosen_index_in_sequence]
                            dna_sequences[chosen_index][chosen_index_in_sequence] = \
                                random.choice(list(filter(lambda nucleotide: nucleotide != chosen_nucleotide,
                                                          ['A', 'C', 'G', 'T'])))

                        # deletion errors
                        for deletion_iteration in range(int(len(dna_sequences) * self.nucleotide_deletion)):
                            chosen_index = random.choice(total_indices)
                            del dna_sequences[chosen_index][random.randint(0, len(dna_sequences[chosen_index]) - 1)]

                        decoded_data = pipeline.transcode(direction="t_s", input_string=dna_sequences,
                                                          index=needed_index)

                        bit_segments = decoded_data["bit"]

                        if bit_segments is None:
                            iter_log = pipeline.output_records()
                            iter_log["transcoding state"] = False
                            iter_log["success rate"] = "0.000%"
                        else:

                            iter_log = pipeline.output_records()
                            iter_log["transcoding state"] = encoded_data["bit"] == bit_segments
                            success_count = 0
                            for final_bit_segment in bit_segments:
                                if final_bit_segment in encoded_data["bit"]:
                                    success_count += 1
                            iter_log["success rate"] = str(round(success_count / len(bit_segments) * 100, 3)) + "%"

                        string = file_name + ", " + scheme_name + ", " + correct_name + ", "
                        string += str(iter_log["information density"]) + ", " + \
                                  str(iter_log["encoding runtime"]) + ", " + \
                                  str(iter_log["decoding runtime"]) + ", " + \
                                  str(iter_log["transcoding state"]) + ", " + \
                                  str(iter_log["success rate"])
                        print(string)
                        pipeline_logs.append(iter_log)

                    result = {
                        "coding scheme": scheme_name, "error-correction": correct_name,
                        "file": file_name, "result": pipeline_logs
                    }
                    results["task " + str(task_index)] = result
                    task_index += 1

                    if self.need_logs:
                        print(">" * 50)
                        print()

        self.records["results"] = results

    def output_records(self, **info):
        if "type" in info:
            param_names = []
            param_values = []

            for key, value in self.records["evaluation parameters"].items():
                param_names.append(key)
                param_values.append(value)

            result_names = [
                "task id", "coding scheme", "error-correction", "file",
                "payload length", "index length", "error-correction length",
                "information density", "encoding runtime", "decoding runtime",
                "error rate", "error indices", "error bit segments",
                "transcoding state", "success rate"
            ]
            result_data_group = []
            for task_id, data in self.records["results"].items():
                result_data = [
                    task_id, data["coding scheme"], data["error-correction"], data["file"],
                ]
                for one_data in data["result"]:
                    one_iteration = [
                        one_data["payload length"], one_data["index length"], one_data["error-correction length"],
                        one_data["information density"], one_data["encoding runtime"], one_data["decoding runtime"],
                        one_data["error rate"], one_data["error indices"], one_data["error bit segments"],
                        one_data["transcoding state"], one_data["success rate"]
                    ]

                    result_data_group.append(result_data + copy.deepcopy(one_iteration))
            if info["type"] == "path":
                if "path" in info:
                    with open(info["path"], "w", encoding="utf-8") as save_file:
                        save_file.write(str(param_names)[1: -1].replace("\'", "") + "\n")
                        save_file.write(str(param_values)[1: -1].replace("\'", "") + "\n")
                        save_file.write(str(result_names)[1: -1].replace("\'", "") + "\n")
                        for result_data in result_data_group:
                            save_file.write(str(result_data)[1: -1].replace("\'", "") + "\n")
                else:
                    raise ValueError("\"path\" is unknown!")
            elif info["type"] == "string":
                if self.need_logs:
                    print("Evaluation log: ")
                    print(str(param_names)[1: -1].replace("\'", ""))
                    print(str(param_values)[1: -1].replace("\'", ""))
                    print(str(result_names)[1: -1].replace("\'", ""))
                    for result_data in result_data_group:
                        print(str(result_data)[1: -1].replace("\'", ""))

        return self.records