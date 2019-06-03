<p align="center">
<img src="https://github.com/ntpz870817/Chamaeleo/blob/master/logo.png" alt="Chamaeleo" title="Chamaeleo" width="60%"/>
</p>

---

# Read before you want to use it
**Chamaeleo** is currently the only collection focused on different codec methods for DNA storage.
We hope to provide a readable, robust and high-performance learning and useful framework for researchers and engineers.

## Environment Configuration
The kit is developed by **Python3.5**.

In addition, the packages we are calling now is as follows:

- [x] sys
- [x] os
- [x] random
- [x] math
- [x] struct
- [x] datetime
- [x] numpy
- [x] pickle

## Kit Tree Diagram
```html
├── docs                              // Description document folder
│    ├── Contributor Manual.md        // Read Before You Want to Make a Contribution
│    ├── User Manual.md               // Read before you want to use it
├── methods                           // Method module
│    ├── property                     // Inherent property folder
│    │    ├── inherent.py             // inherent property
│    │    ├── motif_friendly.py       // Determining whether motif is friendly to sequencing and synthesis
│    ├── double_double.py             // DDC (Double-Double DNA Storage Code)
│    ├── simple.py                    // Simple (Simple DNA Storage Code)
│    ├── yin_yang.py                  // YYC (Yin-Yang DNA Storage Code)
├── utils                             // Util module
│    ├── data_handle.py               // Conversion of DNA motifs and binary document
│    ├── log.py                       // Outputting the logs in console
│    ├── model_saver.py               // Save model to file and load model from file
│    ├── monitor.py                   // Getting the progress  situation and the time left
├── chamaeleo.py                      // Main calling function
├── README.md                         // Description document of kit
```

## Method of Application
In the encoding process, we first instantiate the method, and then pass the method and the necessary path into **chamaeleo**.

Taking Yin-Yang DNA Storage Code as an Example, the specific usage is as follows:

```python
from chamaeleo import *

method = yyc.YYC()

chamaeleo.encode(method, input_path="C:\\init.mp4", output_path="C:\\target.dna", model_path="C:\\yyc.pkl")
```

In the decoding process, we first instantiate the method (init method or path of model file), and then pass the method and the necessary path into **chamaeleo**.

Taking Yin-Yang DNA Storage Code as an Example, the specific usage (using init method) is as follows:

```python
from chamaeleo import *

method = yyc.YYC()

chamaeleo.decode(method, input_path="C:\\target.dna", output_path="C:\\target.mp4")
```

Taking Yin-Yang DNA Storage Code as an Example, the specific usage (using path of model file) is as follows:

```python
from chamaeleo import *

chamaeleo.decode(input_path="C:\\target.dna", output_path="C:\\target.mp4", model_path="C:\\yyc.pkl")
```