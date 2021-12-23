from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os
import random

class uatg_cache_dcache_fill(IPlugin):
    def init(self):
        super().init()
        self._sets = 64
        self._word_size = 8
        self._block_size = 8
        self._ways = 4
    
    def execute(self, core_yaml, isa_yaml):
        _dcache_dict = core_yaml['dcache_configuration']
        _dcache_en = _dcache_dict['instantiate']
        self._sets = _dcache_dict['sets']
        self._word_size = _dcache_dict['word_size']
        self._block_size = _dcache_dict['block_size']
        self._ways = _dcache_dict['ways']

    def check_log(self, log_file_path, reports_dir):
        f = open(log_file_path, "r")
        log_file = f.read()
        f.close()

        test_report = {
                "cache_dcache_fill_02_report": {
                    'Doc': "ASM should have filled the cache of size {0}. This report verifies that.".format(self._sets * self._word_size * self._block_size * self._ways / 8)
                    'Execution status': ''
                    }
                }

    def generate_covergroups(self, config_file):
        ''

    def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:

        asm_data = '\nrvtest_data:\n'

        for i in range (self._block_size * self._sets * self._ways*2):
            asm_data += "\t.word 0x{0:08x}\n".format(random.randrange(16**8))
        
    	asm_main = "\tfence\n\tli, t0, 69\n\li, t1, {0}\n\tli, t5, {1}\n\tli, t6, {2}\n\tla t2, rvtest_data\n".format(self._sets, self._ways, self._sets * self._ways)
    	asm_lab1 = "lab1:\n\tlw t0, 0(t2)\n\taddi t2, t2, {0}\n\taddi t4, t4, 1\n\tblt t4, t5, lab1\n\tli t2,0\n\tadd t2, t2, t6\n\taddi t6, t6, {1}\n\taddi a1, a1, 1\n\tblt a1, t6, end\n\tj lab1\n".format(self._sets * self._word_size *, self._block_size)
    	asm_end = "end:\n\tnop\n\tfence.i\n"
        
        asm = asm_main + asm_lab1 + asm_end
        compile_macros = []

        return [{
            'asm_code': asm,
            'asm_data': asm_data,
            'asm_sig': '',
            'compile_macros': compile_macros
        }]