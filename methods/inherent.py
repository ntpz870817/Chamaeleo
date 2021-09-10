import itertools
import numpy
import Chamaeleo.utils.monitor as monitor

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

gc_codes = ['AAC', 'AAG', 'AAT', 'ACA', 'ACG', 'ACT', 'AGA', 'AGC', 'AGT', 'ATA', 'ATC', 'ATG',
            'CAC', 'CAG', 'CAT', 'CCA', 'CCG', 'CCT', 'CGA', 'CGC', 'CGT', 'CTA', 'CTC', 'CTG',
            'GAC', 'GAG', 'GAT', 'GCA', 'GCG', 'GCT', 'GGA', 'GGC', 'GGT', 'GTA', 'GTC', 'GTG',
            'TAC', 'TAG', 'TAT', 'TCA', 'TCG', 'TCT', 'TGA', 'TGC', 'TGT', 'TTA', 'TTC', 'TTG']


def get_yyc_rule_by_index(index, need_logs=False):
    rules = []
    temp_rule1 = ["".join(x) for x in itertools.product("01", repeat=4)]
    temp_rule2 = ["".join(x) for x in itertools.product("01", repeat=16)]

    m = monitor.Monitor()

    if need_logs:
        print("Find all the available Yin-Yang rules.")

    count = 0
    step = 0
    for base in ["A", "T", "C", "G"]:
        for rule1index in range(len(temp_rule1)):
            for rule2index in range(len(temp_rule2)):
                rule1 = list(map(int, list(temp_rule1[rule1index])))
                rule2 = numpy.array(list(map(int, list(temp_rule2[rule2index])))).reshape(4, 4).tolist()
                if _check(rule1, rule2):
                    rules.append(YYCRule(rule1, rule2, base, count))
                    count += 1

                step += 1

                if need_logs:
                    m.output(step, len(temp_rule1) * len(temp_rule2) * 4)

    if index < 0 or index >= len(rules):
        raise ValueError("We have " + str(len(rules)) + " rules, index " + str(index) + " is wrong!")

    if need_logs:
        print("Current Rule is " + str(rules[index].get_info()) + ".")

    return rules[index].get_info()


def _check(rule1, rule2):
    for index in range(len(rule1)):
        if rule1[index] != 0 and rule1[index] != 1:
            return False

    if sum(rule1) != 2:
        return False

    if rule1[0] == rule1[1]:
        same = [0, 1, 2, 3]
    elif rule1[0] == rule1[2]:
        same = [0, 2, 1, 3]
    else:
        same = [0, 3, 1, 2]

    for row in range(len(rule2)):
        if rule2[row][same[0]] + rule2[row][same[1]] != 1 or rule2[row][same[0]] * rule2[row][same[1]] != 0:
            return False
        if rule2[row][same[2]] + rule2[row][same[3]] != 1 or rule2[row][same[2]] * rule2[row][same[3]] != 0:
            return False

    return True


class YYCRule:

    def __init__(self, rule1, rule2, support_base, identity):
        self.b2i = {'A': 0, 'T': 1, 'C': 2, 'G': 3}
        self.i2b = {0: 'A', 1: 'T', 2: 'C', 3: 'G'}
        self.rule1 = rule1
        self.rule2 = rule2
        self.support_base = support_base
        self.identity = identity

    def lists_to_motif(self, upper_list, lower_list):
        motif = []

        for col in range(len(upper_list)):
            if col > 0:
                motif.append(self.__binary_to_base__(upper_list[col], lower_list[col], motif[col - 1]))
            else:
                motif.append(self.__binary_to_base__(upper_list[col], lower_list[col], self.support_base))
        return motif

    def __str__(self):
        return "[" + self.support_base + ", " + str(self.rule1) + ", " + str(self.rule2) + "]"

    def __binary_to_base__(self, upper_bit, lower_bit, support_base):

        current_options = []
        for index in range(len(self.rule1)):
            if self.rule1[index] == int(upper_bit):
                current_options.append(index)

        if self.rule2[self.b2i.get(support_base)][current_options[0]] == int(lower_bit):
            one_base = self.i2b[current_options[0]]
        else:
            one_base = self.i2b[current_options[1]]

        return one_base

    def get_info(self):
        return [self.support_base, self.rule1, self.rule2]
