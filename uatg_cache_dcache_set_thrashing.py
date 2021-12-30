from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os
import random

class uatg_cache_dcache_set_thrashing(IPlugin):
    def _init_(self):
        super()._init_()
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

        asm_main = "\n\tfence\n\tli t0, 69\n\tli t1, 1\n\tli t3, {0}\n\tla t2, rvtest_data".format(self._sets, self._ways)
        asm_lab1 = "\nlab1:\n\tsw t0, 0(t2)\n\taddi t2, t2, {0}\n\tbeq t4, t3, nop\n\taddi t4, t4, 1\n\tj lab1".format(self._block_size * self._word_size)
        asm_nop = "\nnop:\n\tmv t4, x0\n"
        for i in range(self._fb_size * 2):
            asm_nop += "\tnop\n"

        asm_st = "asm_st:\n"
        for i in range(100):
            asm_st += "\tlw t0, {0}(t2)\n".format(i*(self._word_size*self._block_size*self._sets))
        asm_end = "\nend:\n\tnop\n\tfence.i\n"
        asm = asm_main + asm_lab1 + asm_nop + asm_st + asm_end
        compile_macros = []    	
    	
        return [{
            'asm_code': asm,
            'asm_data': asm_data,
            'asm_sig': '',
            'compile_macros': compile_macros
        }]