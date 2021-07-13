Contributor Manual
==================

![logo](_static/logo.png)


**Chamaeleo** is currently the only collection focused on different codec methods for DNA storage.
We hope to provide a readable, robust and high-performance learning and useful framework for researchers and engineers.
We welcome your participation and dedicate strength to this community.

## Language in USE
We use **Python3.7.3** to develop the kit.

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
- [x] reedsolo

If you have other packages, Please add them here.

While choosing external packages, you need to consider the problems caused by compatibility between different systems and focus on the reliability of the source of the package.
For example, the Windows version of Python has no "termios" module.
Failures of development or usage caused by external packages should be avoid.
In addition, some non-robust external packages may lead to instability or even application crash of the kit.


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

Reference: Z.Ping et al. Towards Practical and Robust DNA-based Data Archiving by Codec Named “Yin-Yang”. doi: https://doi.org/10.1101/829721 2019
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
			Make sure that Two of the bases are 1 and the other two are 0, so there are only 6 case.

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
introduction: Separate 'good' and 'bad' data from total data, and splice index and data as a list

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
import Chamaeleo.utils.monitor as monitor

monitor = monitor.Monitor()
# do something
length = 1000000000000
for index in range(length):
    monitor.output(index, length)
    # do something
```

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
We strongly recommend that you update the [**Contributor Manual**](contributor_manual.md)
or [**User Manual**](user_manual.md) as appropriate while completing the coding.
