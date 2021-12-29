from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os
import random

class uatg_cache_dcache_line_thrashing(IPlugin):
    def __init__(self):
        super().__init__()
        self._sets = 64
        self._word_size = 8
        self._block_size = 8
        self._ways = 4
        self._fb_size = 9
    
    def execute(self, core_yaml, isa_yaml) -> bool:
        _dcache_dict = core_yaml['dcache_configuration']
        _dcache_en = _dcache_dict['instantiate']
        self._sets = _dcache_dict['sets']
        self._word_size = _dcache_dict['word_size']
        self._block_size = _dcache_dict['block_size']
        self._ways = _dcache_dict['ways']
        self._fb_size = _dcache_dict['fb_size']
        return True

    def check_log(self, log_file_path, reports_dir):
        f = open(log_file_path, "r")
        log_file = f.read()
        f.close()

        test_report = {
                "cache_dcache_fill_01_report": {
                    'Doc': "ASM should have filled the fill buffer of size {0}. This report verifies that.".format(self._fb_size),
                    'Execution status': ''
                    }
                }

    def generate_covergroups(self, config_file):
        ''

    def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:

        asm_data = '\nrvtest_data:\n'

        for i in range(self._block_size * self._sets * self._ways*2):
            asm_data += "\t.word 0x{0:08x}\n".format(random.randrange(16**8))

        asm_main = "\tfence\n\tli t0, 69\n\tli t3, {0}\n\tli t1, 1\n\tli t5, {0}\n\tla t2, rvtest_data\n".format(self._ways * self._sets)
        asm_lab1 = "lab1:\n\tsw t0, 0(t2)\n\taddi t2, t2, {0}\n\taddi t0, t0, 1\n\tblt t4, t5, lab1\n".format(self._block_size * self._block_size)
        asm_lab2 = "lab2:\n\tmv t4, x0\n\tlw t0, 0(t2)\n\taddi t2, t2, {0}\n\taddi t0, t0, 1\n\taddi t1, t1, 1\n\tblt t1, t3, lab1\n".format(self._block_size * self._word_size)
        asm_nop = "asm_nop:\n"
        for i in range(self._fb_size * 2):
            asm_nop += "\tnop\n"
    	
        asm_lt = "asm_lt:\n"
        for i in range(self._ways * self._sets * 2):
            asm_lt += "\tsw t0, {0}(t2)\n".format(64 * (i + 1))

        asm_end = "\nend:\n\tnop\n\tfence.i\n"
        asm = asm_main + asm_lab1 + asm_lab2 + asm_nop + asm_lt + asm_end
        compile_macros = []    	
    	
        return [{
            'asm_code': asm,
            'asm_data': asm_data,
            'asm_sig': '',
            'compile_macros': compile_macros
        }]
