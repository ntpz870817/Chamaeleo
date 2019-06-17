"""
Name: Inherent property

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) Common attributes in constraint methods.
.
"""

"""
Conversing base to actual index, where index 0 <-> A, index 1 <-> T, index 2 <-> C, index 3 <-> G.
base_index.get(?)
index_base.get(?)
"""

base_index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
index_base = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}

rotate_codes = {'A': ['C', 'G', 'T'], 'C': ['G', 'T', 'A'], 'G': ['T', 'A', 'C'], 'T': ['A', 'C', 'G']}

goldman_dict = ["22201", "00100", "11220", "00211", "20222", "00222", "02211", "222110",
                "22002", "02100", "22001", "222122", "12001", "02021", "10100", "02010",
                "20101", "12211", "12120", "11111", "21211", "21221", "20220", "00122",
                "20022", "12121", "21111", "00221", "00202", "222202", "222102", "00010",
                "02212", "10011", "22011", "02221", "21212", "21021", "11211", "10111",
                "12220", "22110", "22101", "11122", "22022", "01210", "00210", "02122",
                "10122", "01011", "11101", "01102", "22112", "12122", "11012", "222112",
                "02201", "02011", "20021", "222021", "00022", "222200", "222120", "21010",
                "00121", "02022", "20100", "10211", "21001", "21210", "10212", "222212",
                "20110", "20010", "21220", "21022", "21000", "01211", "10220", "12002",
                "12011", "11212", "21100", "12210", "20112", "22200", "22102", "21222",
                "21012", "12101", "10120", "01202", "10200", "02210", "222211", "11201",
                "00102", "01112", "22010", "00012", "22100", "20001", "20202", "02102",
                "20200", "20210", "20012", "11100", "02101", "11021", "00021", "02110",
                "12102", "01012", "10101", "10222", "10221", "10002", "01120", "00201",
                "10020", "222111", "222220", "02111", "222222", "00000", "10112", "22121",
                "02000", "10000", "20111", "00212", "22021", "21112", "11022", "01220",
                "11102", "20011", "22111", "10021", "12212", "11202", "10201", "02200",
                "02002", "11120", "20102", "11110", "11002", "22000", "21002", "21102",
                "222221", "11020", "20221", "01002", "11001", "00120", "02202", "10202",
                "10012", "22012", "20211", "21201", "00220", "11222", "21011", "10110",
                "20002", "20122", "22122", "20201", "10022", "21101", "12110", "12222",
                "00200", "21202", "10210", "10010", "02012", "12221", "12022", "02222",
                "01100", "02121", "01122", "00112", "01020", "222100", "01222", "21020",
                "01201", "00001", "12021", "12010", "20121", "21120", "00002", "222201",
                "00011", "01010", "12112", "11112", "02120", "11010", "01110", "01212",
                "20120", "12000", "12100", "11210", "11011", "21200", "12200", "01111",
                "01200", "12012", "10121", "10102", "222210", "00020", "01000", "20020",
                "11121", "10001", "02001", "01101", "222121", "21121", "02220", "01001",
                "222101", "01022", "20212", "00101", "222022", "01021", "00111", "11200",
                "12201", "11000", "02112", "01221", "00110", "11221", "01121", "12111",
                "12020", "02020", "22020", "20000", "21110", "22120", "12202", "21122", "222020"]

gc_codes = ['AAT', 'AAC', 'AAG', 'ATA', 'ATT', 'ATC', 'ATG', 'ACA', 'ACT', 'ACC', 'ACG', 'AGA', 'AGT', 'AGC', 'AGG',
            'TAA', 'TAT', 'TAC', 'TAG', 'TTA', 'TTC', 'TTG', 'TCA', 'TCT', 'TCC', 'TCG', 'TGA', 'TGT', 'TGC', 'TGG',
            'CAA', 'CAT', 'CAC', 'CAG', 'CTA', 'CTT', 'CTC', 'CTG', 'CCA', 'CCT', 'CCG', 'CGA', 'CGT', 'CGC', 'CGG',
            'GAA', 'GAT', 'GAC', 'GAG', 'GTA', 'GTT', 'GTC', 'GTG', 'GCA', 'GCT', 'GCC', 'GCG', 'GGA', 'GGT', 'GGC']
