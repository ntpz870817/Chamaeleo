<p align="center">
<img src="https://github.com/ntpz870817/Chamaeleo/blob/master/logo.png" alt="Chamaeleo" title="Chamaeleo" width="60%"/>
</p>

---

# Read Before You Want to Make a Contribution
**Chamaeleo** is currently the only collection focused on different codec methods for DNA storage.
We hope to provide a readable, robust and high-performance learning and useful framework for researchers and engineers.
We welcome your participation and dedicate strength to this community.

## Language in USE
We use **Python3.5** to develop the kit.

## Package in USE
The packages we are calling now is as follows:

- [x] sys
- [x] os
- [x] random
- [x] math
- [x] struct
- [x] datetime
- [x] numpy
- [x] pickle
- [x] csv


If you have other packages, Please add them here.

While choosing external packages, you need to consider the problems caused by different systems and focus on the reliability of the source of the package.
For example, the Windows version of Python has no "termios" module.
Failures of development or usage caused by external packages should be avoid.
In addition, some non-robust external packages may lead to instability or even collapse of the kit.


## Kit Tree Diagram
```html
├── docs                              // Description document folder
│    ├── author.md                    //  Author catalogue
│    ├── contributor_manual.md        // Read Before You Want to Make a Contribution
│    ├── user_manual.md               // Read before you want to use it
├── methods                           // Method module
│    ├── components                    // Inherent property folder
│    │    ├── index_data.py           // Processing the relationship between index and data
│    │    ├── inherent.py             // Inherent property
│    │    ├── motif_friendly.py       // Determining whether motif is friendly to sequencing and synthesis
│    ├── double_double.py             // DDC (Double-Double DNA Storage Code)
│    ├── simple.py                    // Simple (Simple DNA Storage Code)
│    ├── yin_yang.py                  // YYC (Yin-Yang DNA Storage Code)
├── test                              // Test module
│    ├── generated_files              // DNA motif set file or binary file generated in the test
│    │    ├── README.md               // Description document of generated files and the above folder
│    ├── test_files                   // Files for testing
│    ├── test_functional              // Functional test folder
│    │    ├── README.md               // Description document of the above folder
│    ├── test_integrated              // Integrated test folder
│    │    ├── st_ddc.py               // Symmetrical testing of DDC
│    │    ├── st_simple.py            // Symmetrical testing of Simple
│    │    ├── README.md               // Description document of the above folder
├── utils                             // Util module
│    ├── data_handle.py               // Conversion of DNA motifs and binary document
│    ├── log.py                       // Outputting the logs in console
│    ├── model_saver.py               // Save model to file and load model from file
│    ├── monitor.py                   // Getting the progress  situation and the time left
├── .gitignore                        // Upload Ignore File
├── chamaeleo.py                      // Main calling function
├── LICENSE                           // Protocol of kit
├── logo.png                          // Logo of kit
├── README.md                         // Description document of kit
```

## Coding Specification
### Document Header Annotation Specification
Several information should be included in the beginning of the file:
(1) Name, (2) Coder, (3) Current Version, and (4) Function(s).

An overview of a document is necessary, which helps us to know what tasks this document has accomplished.
Among them, the "Name" section should contain citations including journal papers or other reference.
This operation will help people with learning needs to trace back to the principles of methods.


A simple example is shown below:

```python
"""
Name: YYC(Ying-Yang DNA Storage Code)

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) DNA encoding by YYC.
             (2) DNA decoding by YYC.

Advantages: (1) high compressibility, maximum compressibility to 1/2 of the original data.
            (2) preventing repetitive motifs, like ATCGATCG...
            (3) increase the number of sequence changes (1,536 cases), increasing data security.

Reference: Z.Ping et al. Towards Practical and Robust DNA-based Data Archiving by Codec Named “Yin-Yang”. XXX. 2019
"""
```

### Function Header Annotation Specification
Unless the construction and reading of the function is very simple, we need to complete the annotation of the function header.
It is important for cooperative development.
Usually, the annotation includes the purpose of the function, the interpretation and constraints of the input parameters, and the necessary information of the return production.


Two simple example is shown below:
```python
"""
introduction: The initialization method of YYC.

:param base_reference: Correspondence between base and binary data (RULE 1).
                       Make sure that the first and third, and the second and fourth are equal, so there are only two cases:
                       [0, 0, 1, 1] or [1, 1, 0, 0].

:param current_code_matrix: Conversion rule between base and binary data based on support base and current base (RULE 2).
                             Label row is the support base, label col is the current base.
                                 A   T   C   G
                             A   X1  Y1  X2  Y2
                             T   X3  Y3  X4  Y4
                             C   X5  Y5  X6  Y6
                             G   X7  Y7  X8  Y8
                             Make sure that Xn + Yn = 1 and Xn * Yn = 0, n is in [1, 8].

:param support_bases: Base replenishment before official data.
                      Make sure that the count of support base must more than support spacing.
                      Make sure that the number range of each position is {0, 1, 2, 3}, reference base index.

:param support_spacing: Spacing between support base and current base.
                        When the support base is the front of the current base, the spacing is 0.

:param max_ratio: The max ratio of 0 or 1.
                  When the (count/length) >= this parameter, we decide that this binary sequence is not good.

"""
```

and another is:

```python
"""
introduction: Separate good and bad data from total data, and splice index and data as a list

:param matrix: Generated binary two-dimensional matrix
               The data of this matrix contains only 0 or 1 (non-char).
               Type: int or bit

:returns good_datas, bad datas: good and bad data from total data
                                Type: list(int)
"""
```

### Process Output Specification
Part of the process may require  long loading time.
We recommend that you to monitor the running time using [**monitor.py**](https://github.com/ntpz870817/Chamaeleo/blob/master/utils/monitor.py) objects under folder **utils**.

The specific usage is as follows:

```python
import utils.monitor as monitor

monitor = monitor.Monitor()
# do something
length = 1000000000000
for index in range(length):
    monitor.output(index, length)
    # do something
```

### Log Output Specification
We want you to print each core step to the console through [**log.py**](https://github.com/ntpz870817/Chamaeleo/blob/master/utils/log.py)  in folder **utils**.
This helps us understand what procedure the kit takes.

The specific usage is as follows:

```python
import sys
import utils.log as log

log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
           "Restore the disrupted data order.")

log.output(log.WARN, str(__name__), str(sys._getframe().f_code.co_name),
           "There may be a large number of motifs that are difficult to use. "
           "We recommend stopping and modifying the rules.")

log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
           "The file selection operation was not performed correctly. Please complete the operation again!")
```
We have declared three types available now: NORMAL, WARN, and ERROR.
If the type is ERROR, we will end this program immediately.
- If the type is NORMAL, print normal.
- If the type is WARN, print yellow and high light.
- If the type is ERROR, print red and high light.

### Variable Naming Specification
* The naming of variables requires the basic expression of the meaning of variables.
  We do not recommend that you use some simple characters like "i", "j" or "k" as process variables, which can be obscure and not conducive to cooperative development.
* Variables are represented by lowercase letters, numbers and underscores.
* If you iterate based on subscripts, we recommend that you name the variable "index".
* If some variables modify or save the original object (\*), it is recommended to use "current_\*", "last_\*", or "temp_\*".

## Testing Process and Recommendations
The complete process of testing is as follows:
(1) setting input type, (2) single function test, (3) integration function test, (4) error input test (input reminder and optimization),
(5) unilateral integration function test (encoding or decoding), (6) symmetrical integration function test (corresponding to encoding and decoding process)

We strongly recommend that you complete all the tests before submitting them.

In addition, considering that using “print” or “log” functions for testing is irrational.
Package [**"PySnooper"**](https://github.com/cool-RR/PySnooper) would an option for testing.

## Other Requirements
We strongly recommend that you update the [**Contributor Manual**](https://github.com/ntpz870817/Chamaeleo/blob/master/docs/contributor_manual.md)
or [**User Manual**](https://github.com/ntpz870817/Chamaeleo/blob/master/docs/user_manual.md) as appropriate while completing the coding.
