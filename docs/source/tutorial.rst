.. _sec-Tutorial:

Tutorial
========

General Information
*****************************
Compared to the orthodox information storage media, DNA has extremely high information capacity and durability. From the beginning of the 21st Century, many scientists devoted to studying how to store digit information more effectively in DNA. The coding scheme is a vital part of research in DNA storage, which is transcoding digit to DNA following particular algorithm. It is the first and last steps in storing digit information as DNA.

Some well-accepted coding schemes had been proposed in recent years. These schemes are focusing on optimizing the coding efficiency under certain constrains. Simple code, Goldman's code, and Grass' code use random mechanism, rotating encoding, and DNA codon wheel in Galois Field of size 47, respectively, to eliminate the homopolymer. Erlich's code based on LT code, using screening operation to restrict the occurrence of homopolymer and limit GC content. Yin-Yang code provides 1,536 types of derived rules by the combination of Yin and Yang rule, and finds the best rule based on byte frequency.

Although these schemes are implemented as a program, these individual programs do not have excellent code architecture from the perspective of software engineering. A few program-based validation and improved work will be hindered. And these programs exist independently and are implemented in different programming languages. Therefore, it is difficult to compare these performances in practice or customize them in specific requirements.

We introduce Chamaeleo, an open-source library focused on different coding schemes for DNA storage. This library provides a useful platform for researchers to study different coding schemes and its efficient implementation is suitable for supporting real-world DNA storage applications.


Basic Trancoding
*****************************

The basic transcoding refers to a one-time binary-DNA transcoding process. Besides, it is optional to use error-correction module and to add row index before every segment during encoding process. Under these circumstances, it is feasible to use codec_factory.py (Location: Chamaeleo/) directly.
For decoding part, user can choose to build a new transcoding function or upload a serialize function for decoding.
This statement may be executed through Python programming tools such as PyCharm or by command lines. Considering multiple parameter are used in this statement, it is suggested to use Python programming tools for these tasks. Take 'Yin-Yang' coding as an example, the particular usage is demonstrated as follows:


By programming tools:

.. code-block:: python

  	# encode part
	import Chamaeleo.methods.yyc as yyc
	import Chamaeleo.codec_factory as codec_factory

	method = yyc.YYC()
	codec_factory.decode(method, input_path="C:\\target.dna", output_path="C:\\target.mp4")

	# decode part
  	codec_factory.decode(method, input_path="C:/target.dna", output_path="C:/target.mp4")
	# codec_factory.decode(input_path="C:/target.dna", output_path="C:/target.mp4", model_path="C:/yyc.pkl")



By command line:

.. code-block:: python

  # encode part
  Chamaeleo.codec_factory.encode(Chamaeleo.methods.yyc.YYC(), input_path="C:/init.mp4", output_path="C:/target.dna", model_path="C:/yyc.pkl")

  # decode part
  Chamaeleo.methods.codec_factory.decode(Chamaeleo.methods.yyc.YYC(), input_path="C:/target.dna", output_path="C:/target.mp4")
  Chamaeleo.methods.codec_factory.decode(input_path="C:/target.dna", output_path="C:/target.mp4", model_path="C:/yyc.pkl")


The essential parameters are: method, input_path, output_path, model_path and segment_length. Optional hyper-parameters are: verify and need_index.
The parameters should be consistent for both encoding and decoding processes except input_path and output_path. The input_path of decoding process should be the output_path of encoding process.
For example, if parameter verify is chosen to be the instantiation method for error detection and correction in encoding process (e.g. hamming code), for decoding process, it is necessary to key in this parameter.


Highly customized applications
***********************************************
The basic function of codec_factory.py may not satisfy the highly customized DNA storage transcoding. If user needs to customize the transcoding (e.g. iteration of different algorithm), it is suggested to use Python programming tools such as PyCharm for these tasks.

Log output
--------------------------------
In some of the algorithms, users can choose to output log for the convenience of monitoring the operation of program.
In these algorithms, it is optional to use the parameter, need_log.

Cutomized transcoding
---------------------

In transcoding module, four transcoding algorithms are collected. The particular hyper-parameters of these four algorithms are introduced as below:

Simple Code is re-established via algorithms reported by Church et. al.
Hyper-parameter, mapping_rule, in simple code describes the relationship between nucleotide and binary digit. The default setting is [0,0,1,1], which means ['A'=0, 'C'=0, 'G'=1, 'T'=1].
When user has customized request for mapping rules, it will be feasible to use this hyper-parameter to pass the data:

.. code-block:: python

	sc.SC(mapping_rule=[1,0,1,0])

which means that the customized mapping rule is ['A'=1, 'T'=0, 'G'=1, 'T'=0]


Huffman Code is re-established via algorithm reported by Goldman et. al.
Hyper-parameter, fixed_huffman, in Huffman code describes whether to use the fixed huffman rule obtained from Goldman's paper, the default value is True.
When user decides to generate huffman tree according to specific file, the command will be:

.. code-block:: python

	hc.HC(fixed_huffman=False)

Grass Code is re-established via algorithm reported via algorithm reported by Grass et. al.
Hyper parameter, base_value, in Grass code describes the mapping relationship between GF47 and nucleotide-triplet, the default value is [_ for _ in range(48)].
When user needs to customize the mapping relationship, for example, the command could be:

.. code-block:: python

	# inverse mapping
	mapping = [47 - i for i in range(48)]
	gc.GC(base_values=mapping)

Yin-Yang Code is the algorithm describes the collection of derivative rules reported by Ping et. al.
Six hyper-parameters are included in this method: base_reference, current_code_matrix，support_bases，support_spacing，max_ratio,  and search_count.
bse_referece: Yang rule, correspondence between base and bit data in the binary segment I. The default value is Rule 495, [0, 1, 0, 1].
current_code_matrix: Yin rule, correspondence between base and bit data in the binary segment II. The default value is Rule 495, [[1, 1, 0, 0], [1, 0, 0, 1], [1, 1, 0, 0], [1, 1, 0, 0]].
support_bases: indicates the virtual base used for both encoding and decoding before real information, the default value is 'A'.
support_spacing: indicates the spacing between support nucleotide and current nucleotide. If support nucleotide is directly one position before current nucleotide, the spacing would be 0. If support_bases = 'AA', then the supporting_spacing would be 1.
max_ratio: indicates the criteria of determine whether a binary segment is considered to be 'good' or 'bad' for incorporation. For example, the default value of max_ratio is 0.8, which means that if '0' or '1' exceeds 80% of the binary segment, the segment will be considered to be 'bad' for incoporation.
search_count: indicates how many times the program will do to search for incorporation. This parameter is used for avoid infinite loop and save time. The default value is 2.
When user need to customize YYC transcoding process, an example of command could be:

.. code-block:: python

	yyc.YYC(base_reference=[0, 0, 1, 1], current_code_matrix=[[0, 1, 0, 1],[0, 1, 0, 1],[0, 1, 0, 1],[0, 1, 0, 1]],
		support_bases="AC", support_spacing=1, max_ratio=0.7, search_count=20)

Customized error-correction method
-------------------------------------
Error-correction is one of the optional but important module in DNA storage.
In Chamaeleo, it provides two error detection/correnction methods: Hamming Code and Reed-Solomon Code. More error-correction codes such as LDPC, BCH, Turbo codes can be added for follow-up.

In general, for every method, the program provides two categories of application include three different functions each: add_for_matrix, remove_for_matrix and verify_for_matrix; add_for_list, remove_for_list and verify_for_list.
add function is used for adding error-correction during encoding; remove function is used for removing error-correction code in data during decoding; verify function is used for verification of errors in current data using specified error-correction code, it will automatically correct the errors found and give reminders to users if the correction operation fails.

When users choose hamming code for error correction, it will generate output data carrying hamming error-correction code according to users' input information automatically.
An example would be:

.. code-block:: python

	code = hm.Hm()
	v_matrix = code.add_for_matrix(o_matrix)
	c_matrix = code.verify_for_matrix(v_matrix)

For Reed-Solomon Code, the library provides a hyper-parameter to indicate the length of error-correction code, the default value is 3.
In real application, user can gain more powerful ability of error-correction (i.e. to correct more errors in one segments) by increasing check_size, the value of check_size equals to the number of errors the function can correct.
An example of using Reed-Solomon Code would be:

.. code-block:: python

	code = rs.RS(check_size=10)
	v_matrix = code.add_for_matrix(o_matrix)
	c_matrix = code.verify_for_matrix(v_matrix)

If you set Reed-Solomon Code in your encoding process with out saving model, you need to remember additional length mentioned in the prompt. This value (v) needs to be inputted in RS(additional_size=v) in the decoding process.
