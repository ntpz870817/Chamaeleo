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

base_index = {'A': 0, 'T': 1, 'C': 2, 'G': 3}
index_base = {0: 'A', 1: 'T', 2: 'C', 3: 'G'}
rotate_code = {'A': ['C', 'G', 'T'],  'C': ['G', 'T', 'A'], 'G': ['T', 'A', 'C'], 'T': ['A', 'C', 'G']}
