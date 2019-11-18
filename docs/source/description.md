Description
===========

Chamaeleo provides broaden applications for users to design sequences for DNA-based data storage by personalizing the coding scheme selection, adding row indices for each binary segment, using different error-correction codes, and giving different formats of result for synthesis or further theoretical studies.

This library has two simple and modular processes, which are encoding process and decoding process. The detailed working pipeline of this library is shown in the following figure:

Encoding process
--------------------

Firstly, a specific digital file provided by user is converted to a bit matrix by data processing module. Then, it is optional to add row indices (bit format), because some coding schemes not required row indices, like DNA Fountain. After that, error-correction code can be added to each row of the above bit matrix optionally in error-correction module to ensure the fidelity. Currently, two well-accepted error-correction codes, Hamming code and Reed-Solomon code are included. Finally, in transcoding module, this library applies the transcoding code initialized by users to convert the final bit matrix into DNA segments. These generated DNA segments are outputted into a target file through data processing module.

Decoding process
--------------------

The decoding process is almost a reverse process to the encoding process. Firstly, a DNA segment file is read by data processing module and converted into a bit matrix though transcoding module. Then, error-correction code is executed based on the corresponding encoding process. If the specific error-correction code was added to the encoding process, it also needs to be initialized and used in the decoding process. If one row of bit matrix contains error and cannot be corrected, this row of bit matrix will be notified to the user. In addition, this row will be discarded. After that, if the bit matrix includes row indices in the encoding process, it will be sorted by its row indices in this step. And all the row indices will be deleted after this step. Finally, the (restored) bit matrix is converted to a target digital file by data processing module.
