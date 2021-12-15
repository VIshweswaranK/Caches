from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os

class uatg_cache_dcache_fill(IPlugin):
    def __init__(self):
        super().__init__()
        self._sets = 64
        self._word_size = 8
        self._block_size = 8
        self._ways = 4
        self._fb_size = 9
    
    def execute(self, core_yaml, isa_yaml):
        _dcache_dict = core_yaml['dcache_configuration']
        _dcache_en = _dcache_dict['instantiate']
        self._sets = _dcache_dict['sets']
        self._word_size = _dcache_dict['word_size']
        self._block_size = _dcache_dict['block_size']
        self._ways = _dcache_dict['ways']
        self._fb_size = _dcache_dict['fb_size']

    def check_log(self, log_file_path, reports_dir):
        f = open(log_file_path, "r")
        log_file = f.read()
        f.close()

        test_report = {
                "cache_dcache_fill_01_report": {
                    'Doc': "ASM should have filled the fill buffer of size {0}. This report verifies that.".format(self._fb_size)
                    'Execution status': ''
                    }
                }

    def generate_covergroups(self, config_file):
        ''

    def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
    	asm_main = "fence\n\tcsrr x30, mhpmcounter22\n\tli t0, 69\n\tli t3, {0}\n\tli t1, {1}\n\tli t5, {2}\n".format(self._sets * self._ways - 1, self._sets * self._ways + self_fb_size, self._ways)
    	asm_lab1 = "lab1:\n\tsw t0, 0(t2)\n\taddi t2, t2, {0}\n\tbeq t4, t3, lab2\n\taddi t4, t4, 1\n\tj lab1\n".format(self._sets * self._ways)
    	asm_lab2 = "lab2:\n\tli t2, 0\n\tsw t0, 0(t2)\n\taddi t2, t2, {0}\n\tbeq t4, t1, reinit\n\taddi t4, t4, 1\n\tj lab2\n".format(self._sets * self._ways)
    	asm_reinit = "reinit:\n\tli a1, {0}\n\tli t2, 0\n\tj lab3\n".format(self._sets * self._word_size * self._block_size)
    	asm_lab3 = "lab3:\n\taddi t0, t0, 1\n\tsw t0, 0(t2)\n\tbeq t4, a1, reinit2\n\taddi t4, t4, 1\n\tj lab3\n"
    	asm_reinit2 = "reinit2:\n\tli t4, 1\n\tbeq t6, t3, end\n\taddi t2, t2, {0}\n\taddi t6, t6, 1\n\tj lab3\n".format(self._sets * self._ways)
    	asm_end = "end:\n\tcsrr x31, mhpmcounter22\n\tnop"
    	
	asm = asm_main + asm_lab1 + asm_lab2 + asm_reinit + asm_lab3 + asm_reinit2 + asm_end
        compile_macros = []    	
    	
    	return [{
            'asm_code': asm,
            'asm_sig': '',
            'compile_macros': compile_macros
        }]
