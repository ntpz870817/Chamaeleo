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
│    ├── demo_case_fc.py              // Demo case of Erlich' Code
│    ├── demo_case_gc.py              // Demo case of Grass' Code
│    ├── demo_case_hc.py              // Demo case of Goldman's Code
│    ├── demo_case_sc.py              // Demo case of Simple (Church's) Code
│    ├── demo_case_sc_with_hm.py      // Demo case of Simple (Church's) Code with Hamming Code
│    ├── demo_case_sc_with_rs.py      // Demo case of Simple (Church's) Code with Reed-Solomon Code
│    ├── demo_case_yyc.py             // Demo case of Yin-Yang Code
├── methods                           // Method module
│    ├── components                   // Inherent property folder
│    │    ├── index_operator.py       // Processing the relationship between index and data
│    │    ├── inherent.py             // Inherent property
│    │    ├── validity.py             // Determining whether a DNA sequence is easy or not for sequencing and synthesis
│    ├── verifies                     // Error-Correction Method
│    │    ├── hm.py                   // Hamming error correction
│    │    ├── rs.py                   // Reed-Solomon error correction
│    ├── fc.py                        // FC (DNA Storage Code based on Fountain code, created by Erlich et. al)
│    ├── gc.py                        // GC (DNA Storage Code created by Grass)
│    ├── hc.py                        // HC (DNA Storage Code based on Huffman code)
│    ├── sc.py                        // SC (Simple DNA Storage Code)
│    ├── yyc.py                       // YYC (Yin-Yang DNA Storage Code)
├── utils                             // Util module
│    ├── data_handle.py               // Conversion between DNA sequences and binary document
│    ├── log.py                       // Outputting the logs in console
│    ├── model_saver.py               // Saving model to file and load model from file
│    ├── monitor.py                   // Getting the progress situation and the time left
├── codec_factory.py                  // Main calling function
├── README.md                         // Description document of library
```

## Method of Application
In encoding process, we first instantiate the method, and then pass the method and the necessary path into **chamaeleo**.

Taking Yin-Yang DNA Storage Code as an Example, the specific usage is as follows:

```python
import Chamaeleo.methods.yyc as yyc
import Chamaeleo.codec_factory as codec_factory

method = yyc.YYC()

codec_factory.encode(method, input_path="C:\\init.mp4", output_path="C:\\target.dna", model_path="C:\\yyc.pkl")
```

In decoding process, we first instantiate the method (init method or path of model file), and then pass the method and the necessary path into **chamaeleo**.

Taking Yin-Yang DNA Storage Code as an Example, the specific usage (using init method) is as follows:

```python
import Chamaeleo.methods.yyc as yyc
import Chamaeleo.codec_factory as codec_factory

method = yyc.YYC()

codec_factory.decode(method, input_path="C:\\target.dna", output_path="C:\\target.mp4")
```

Taking Yin-Yang DNA Storage Code as an Example, the specific usage (using path of model file) is as follows:

```python
import Chamaeleo.codec_factory as codec_factory

codec_factory.decode(input_path="C:\\target.dna", output_path="C:\\target.mp4", model_path="C:\\yyc.pkl")
```

Sometimes, we need to add error-correcting validation and serial numbers for each piece of data (for recovery).

In the encoding process, we need to to instantiate the validation function:

```python
import Chamaeleo.codec_factory as codec_factory
import Chamaeleo.methods.verifies.rs as hm

method = yyc.YYC()
verify = hm.Hm()

codec_factory.decode(method, input_path="C:\\target.dna", output_path="C:\\target.mp4", model_path="C:\\yyc+hm.pkl", verify=verify, need_index=True)
```

Also in the decoding process:

```python
import Chamaeleo.codec_factory as codec_factory
import Chamaeleo.methods.verifies.rs as rs

codec_factory.decode(input_path="C:\\target.dna", output_path="C:\\target.mp4", model_path="C:\\yyc+hm.pkl", has_index=True)
```
