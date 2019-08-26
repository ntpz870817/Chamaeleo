User manual
===========

<p align="center">
<img src="https://github.com/ntpz870817/Chamaeleo/blob/master/logo.png" alt="Chamaeleo" title="Chamaeleo" width="60%"/>
</p>

---

# Read before you want to use it
**Chamaeleo** is currently the only collection focused on different codec methods for DNA storage.
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
│    ├── author.md                    // Author catalogue
│    ├── contributor_manual.md        // Read Before You Want to Make a Contribution
│    ├── user_manual.md               // Read before you want to use it
├── methods                           // Method module
│    ├── components                   // Inherent property folder
│    │    ├── index_operator.py       // Processing the relationship between index and data
│    │    ├── inherent.py             // Inherent property
│    │    ├── motif_validity.py       // Determining whether motif is friendly to sequencing and synthesis
│    ├── verifies                     // Error-Correction Method
│    │    ├── hm.py                   // Hamming error correction
│    │    ├── rs.py                   // Reed-Solomon error correction
│    ├── gc.py                        // GC (DNA Storage Code created by Grass)
│    ├── hc.py                        // HC (DNA Storage Code based on Huffman code)
│    ├── sc.py                        // SC (Simple DNA Storage Code)
│    ├── yyc.py                       // YYC (Yin-Yang DNA Storage Code)
├── utils                             // Util module
│    ├── data_handle.py               // Conversion of DNA motifs and binary document
│    ├── log.py                       // Outputting the logs in console
│    ├── model_saver.py               // Save model to file and load model from file
│    ├── monitor.py                   // Getting the progress situation and the time left
├── codec_factory.py                  // Main calling function
├── README.md                         // Description document of library
```

## Method of Application
In the encoding process, we first instantiate the method, and then pass the method and the necessary path into **chamaeleo**.

Taking Yin-Yang DNA Storage Code as an Example, the specific usage is as follows:

```python
from chamaeleo import *

method = yyc.YYC()

codec_factory.encode(method, input_path="C:\\init.mp4", output_path="C:\\target.dna", model_path="C:\\yyc.pkl")
```

In the decoding process, we first instantiate the method (init method or path of model file), and then pass the method and the necessary path into **chamaeleo**.

Taking Yin-Yang DNA Storage Code as an Example, the specific usage (using init method) is as follows:

```python
from chamaeleo import *

method = yyc.YYC()

codec_factory.decode(method, input_path="C:\\target.dna", output_path="C:\\target.mp4")
```

Taking Yin-Yang DNA Storage Code as an Example, the specific usage (using path of model file) is as follows:

```python
from chamaeleo import *

codec_factory.decode(input_path="C:\\target.dna", output_path="C:\\target.mp4", model_path="C:\\yyc.pkl")
```

Sometimes, we need to add error-correcting validation and serial numbers for each piece of data (for recovery).

In the encoding process, we need to to instantiate the validation function:

```python
from chamaeleo import *

method = yyc.YYC()
verify = rs.RS(3)

codec_factory.decode(method, input_path="C:\\target.dna", output_path="C:\\target.mp4", verify=verify, need_index=True)
```

Also in the decoding process:

```python
from chamaeleo import *

verify = rs.RS(3)

codec_factory.decode(input_path="C:\\target.dna", output_path="C:\\target.mp4", model_path="C:\\yyc.pkl", verify=verify, has_index=True)
```
