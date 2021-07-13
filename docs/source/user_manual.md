User manual
===========

![logo](_static/logo.png)


---

**Chamaeleo** is currently the only collection focusing on different codec methods for DNA storage.
We hope to provide a readable, robust and high-performance learning and useful framework for researchers and engineers.

## Environment Configuration
The kit is developed by **Python3.7.3**.

In addition, the packages we are calling now is as follows:

- [x] sys
- [x] os
- [x] random
- [x] math
- [x] struct
- [x] datetime
- [x] numpy
- [x] pickle
- [x] reedsolo

## Library Tree Diagram
```html
├── docs                              // Description document folder
│    ├── source                       // Source code for docs
│    │    ├── author.md               // Author catalogue
│    │    ├── conf.py                 // ReadTheDoc building configure
│    │    ├── contributor_manual.md   // Read before you want to make a contribution
│    │    ├── description.md          // Description the trans-coding process
│    │    ├── index.rst               // Information in the index.html
│    │    ├── installation.md         // Read before you want to build it
│    │    ├── modules.rst             // Information in the modules.html
│    │    ├── tutorial.rst            // Information in the tutorial.html
│    │    ├── user_manual.md          // Read before you want to use it
├── examples                          // Example module
│    ├── generated_files              // DNA sequence set file or binary file generated in the test
│    │    ├── README.md               // Description document of generated files and the above folder
│    ├── log_files                    // Examples of log files
│    │    ├── robustness.logs         // An example of robustness logs (can be open by txt)
│    │    ├── seq_features.logs       // An example of DNA sequence feature logs (can be open by txt)
│    ├── demo_case_basic_feature.py   // Demo case of sequence analysis based on Mona Lisa figure encoded by different algorithms
│    ├── demo_case_best_choice.py     // Demo case of best choice comparison based on Mona Lisa figure encoded by base code and Church code
│    ├── demo_case_robustness.py      // Demo case of robustness analysis based on Mona Lisa figure encoded by base code and Church code 
│    ├── demo_case_transcode.py       // Demo case of transcoding pipeline using different algorithms
├── methods                           // Method module
│    ├── default.py                   // Interfaces of Chamaeleo package
│    ├── ecc.py                       // Implements of error-correction code
│    ├── fixed.py                     // Implements of trans-coding algorithm with fixed rules
│    ├── flowed.py                    // Implements of trans-coding algorithm with screening operation
│    ├── inherent.py                  // Inherent property obtained by original paper
├── test                              // Test module
│    ├── generated_files              // DNA sequence set file or binary file generated in the test
│    │    ├── README.md               // Description document of generated files and the above folder
│    ├── test_ecc_hamming.py          // Functional test for the verification of Hamming Code
│    ├── test_ecc_reed_solomon.py     // Functional test for the verification of Reed-Solomon Code
│    ├── test_indexer.py              // Functional test for adding indices, removing indices, and sorting based on indices 
│    ├── test_screen.py               // Functional test for screening operation
│    ├── test_trans_base.py           // Functional test for the trans-coding of Base Code
│    ├── test_trans_blawat.py         // Functional test for the trans-coding of Blawat Code
│    ├── test_trans_church.py         // Functional test for the trans-coding of Church Code
│    ├── test_trans_dna_fountain.py   // Functional test for the trans-coding of DNA Fountain Code
│    ├── test_trans_goldman.py        // Functional test for the trans-coding of Goldman Code
│    ├── test_trans_grass.py          // Functional test for the trans-coding of Grass Code
│    ├── test_trans_yin_yang_code.py  // Functional test for the trans-coding of Yin-Yang Code
├── utils                             // Util module
│    ├── data_handle.py               // Conversion of DNA sequences and binary document
│    ├── indexer.py                   // Processing the relationship between index and data
│    ├── monitor.py                   // Getting the progress situation and the time left
│    ├── pipelines.py                 // Operation pipelines of transcoding, analysing, and evaluation
│    ├── screen.py                    // Screening operation, which determines whether a DNA sequence is easy or not for sequencing and synthesis
├── .gitignore                        // Upload ignore file
├── codec_factory.py                  // Main calling function
├── LICENSE                           // Protocol of kit
├── logo.png                          // Logo of kit
├── README.md                         // Description document of library
```

## Method of Application
In encoding process, we first instantiate the method, and then pass the method and the necessary path into **chamaeleo**.

Taking Yin-Yang DNA Storage Code as an Example, the specific usage is as follows:

```python
from Chamaeleo.utils.pipelines import TranscodePipeline
from Chamaeleo.methods.flowed import YinYangCode


coding_scheme = YinYangCode()
needed_index = True

read_file_path = "SOURCE.xx"
dna_path = "XXXXXX.dna"
    
pipeline = TranscodePipeline(coding_scheme=coding_scheme, error_correction=None, need_logs=True)

encoded_data = pipeline.transcode(direction="t_c", input_path=read_file_path, output_path=dna_path,
                                  segment_length=120, index=needed_index)
```

In decoding process, we first instantiate the method, and then pass the method and the necessary path into **chamaeleo**.

Taking Yin-Yang DNA Storage Code as an Example, the specific usage (using init method) is as follows:

```python
from Chamaeleo.utils.pipelines import TranscodePipeline
from Chamaeleo.methods.flowed import YinYangCode


coding_scheme = YinYangCode()
needed_index = True

write_file_path = "TARGET.xx"
dna_path = "XXXXXX.dna"
    
pipeline = TranscodePipeline(coding_scheme=coding_scheme, error_correction=None, need_logs=True)

decoded_data = pipeline.transcode(direction="t_s", input_path=dna_path, output_path=write_file_path,
                                  index=needed_index)
```

Sometimes, we need to add error-correcting validation and serial numbers for each piece of data (for recovery).

In the encoding process, we need to to instantiate the validation function:

```python
from Chamaeleo.utils.pipelines import TranscodePipeline
from Chamaeleo.methods.flowed import YinYangCode
from Chamaeleo.methods.ecc import Hamming


coding_scheme = YinYangCode()
error_correction = Hamming()
needed_index = True

read_file_path = "SOURCE.xx"
dna_path = "XXXXXX.dna"
    
pipeline = TranscodePipeline(coding_scheme=coding_scheme, error_correction=error_correction, need_logs=True)

encoded_data = pipeline.transcode(direction="t_c", input_path=read_file_path, output_path=dna_path,
                                  segment_length=120, index=needed_index)
```

Also in the decoding process:

```python
from Chamaeleo.utils.pipelines import TranscodePipeline
from Chamaeleo.methods.flowed import YinYangCode
from Chamaeleo.methods.ecc import Hamming


coding_scheme = YinYangCode()
error_correction = Hamming()
needed_index = True

write_file_path = "TARGET.xx"
dna_path = "XXXXXX.dna"
    
pipeline = TranscodePipeline(coding_scheme=coding_scheme, error_correction=error_correction, need_logs=True)

decoded_data = pipeline.transcode(direction="t_s", input_path=dna_path, output_path=write_file_path,
                                  index=needed_index)
```

For more examples in other pipelines, please see [**here**](https://github.com/ntpz870817/Chamaeleo/tree/master/examples).
