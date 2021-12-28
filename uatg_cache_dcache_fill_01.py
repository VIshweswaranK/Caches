from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os
import random

class uatg_cache_dcache_fill_01(IPlugin):
    def __init__(self):
        super().__init__()
        self._sets = 64
        self._word_size = 8
        self._block_size = 8
        self._ways = 4
    
    def execute(self, core_yaml, isa_yaml) -> bool:
        _dcache_dict = core_yaml['dcache_configuration']
        _dcache_en = _dcache_dict['instantiate']
        self._sets = _dcache_dict['sets']
        self._word_size = _dcache_dict['word_size']
        self._block_size = _dcache_dict['block_size']
        self._ways = _dcache_dict['ways']
        return True

    def check_log(self, log_file_path, reports_dir):
        f = open(log_file_path, "r")
        log_file = f.read()
        f.close()

        test_report = {
                "cache_dcache_fill_01_report": {
                    'Doc': "ASM should have filled the cache of size {0}. This report verifies that.".format(self._sets * self._word_size * self._block_size * self._ways / 8)
                    'Execution status': ''
                    }
                }

    def generate_covergroups(self, config_file):
        ''

    def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:

        asm_data = '\nrvtest_data:\n'

        for i in range(self._block_size * self._sets * self._ways*2):
            asm_data += "\t.word 0x{0:08x}\n".format(random.randrange(16**8))

        asm_main = "\tfence\n\tli t0, 69\n\tli t1, 1\n\tli t3, {0}\n\tla t2, rvtest_data\n".format(self._sets * self._ways)
        asm_lab1 = "lab1:\n\tsw t0, 0(t2)\n\taddi t2, t2, {0}\n\tbeq t4, t3, end\n\taddi t4, t4, 1\n\tj lab1\n".format(self._sets * self._word_size * self._block_size)
        asm_end = "end:\n\tnop\n\tfence.i\n"
        
        asm = asm_main + asm_lab1 + asm_end
        compile_macros = []

        return [{
            'asm_code': asm,
            'asm_data': asm_data,
            'asm_sig': '',
            'compile_macros': compile_macros
        }]
