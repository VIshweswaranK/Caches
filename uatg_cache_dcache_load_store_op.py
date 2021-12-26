from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os

class uatg_cache_dcache_fill(IPlugin):
    def _init_(self):
        super()._init_()
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
    	asm_main = "li t1, 8000\n\tli t2, 0x9999999999999999\n"
        asm_pass1 = "pass1:\n\tli a2, 0x99\n\tsb t2, {0}(t1)\n\tlbu t3, {0}(t1)\n\tbne a2, t3, end\n".format(self._word_size * self._block_size * 1)
        asm_pass2 = "pass2:\n\tli a2, 0x9999\n\tsh t2, {0}(t1)\n\tlhu t3, {0}(t1)\n\tbne a2, t3, end\n".format(self._word_size * self._block_size * 2)
        asm_pass3 = "pass3:\n\tli a2, 0x99999999\n\tsw t2, {0}(t1)\n\tlwu t3, {0}(t1)\n\tbne a2, t3, end\n".format(self._word_size * self._block_size * 3)
        asm_pass4 = "pass4:\n\tli a2, 0x9999999999999999\n\tsd t2, {0}(t1)\n\tld t3, {0}(t1)\n\tbne a2, t3, end\n".format(self._word_size * self._block_size * 4)
        asm_pass5 = "pass5:\n\tli a2, 0xFFFFFFFFFFFFFF99\n\tlb t3, {0}(t1)\n\tbne t3, a2, end\n".format(self._word_size * self._block_size * 1)
        asm_pass6 = "pass6:\n\tli a2, 0xFFFFFFFFFFFF9999\n\tlh t3, {0}(t1)\n\tbne t3, a2, end\n".format(self._word_size * self._block_size * 2)
        asm_pass7 = "pass7:\n\tli a2, 0xFFFFFFFF99999999\n\tlw t3, {0}(t1)\n\tbne t3, a2, end\n".format(self._word_size * self._block_size * 3)
        asm_pass8 = "pass8:\n\tli a2, 0x9999999999999999\n\tld t3, {0}(t1)\n\tbne t3, a2, end\n".format(self._word_size * self._block_size * 4)
        
        asm_pass9 = "pass9:\n\tli a2, 0x99999999\n\t"
        for i in range(7)
            asm_pass9 += "lb s1, {0}(t1)\n\tadd s6, s6, s1\n\tslli ,s6, s6, 8\n\t".format(self._block_size*self._word_size*4+(8*i))
        asm_pass9 += "lb s1, {0}(t1)\n\tadd s6, s6, s1\n\tbne s6, a2, end\n".format(self._word_size*self._block_size*4 + (8*7))
        
        asm_pass10 = "pass10:\n\tli a2, 0x99999999\n\t"
        for i in range(3)
            asm_pass10 += "lh s1, (t1)\n\tadd s6, s6, s1\n\tslli ,s6, s6, 16\n\t".format(self._word_size*self._block_size*4+(16*i))
        asm_pass10 += "lb s1, {0}(t1)\n\tadd s6, s6, s1\n\tbne s6, a2, end\n".format((self._word_size*self._block_size*4 + 16*3))
        
        asm_pass11 = "pass11:\n\tli a2, 0x99999999\n\tlw s1, {0}(t1)\n\tadd s6, s6, s1\n\tslli s6, s6, 32\n\tlw s1, {0}(t1)\n\tadd s6, s6, s1\n\tbne s6, s2, end\n".format(self._word_size*self._block_size*4, (self._word_size*self._block_size*4)+32)
        asm_pass12 = "pass12:\n\tmv t3, zero\n\tli a2, 0x1111\n\tsh t2, {0}(t1)\n\tld t3, {0}(t1)\n\tbeqz t3, end\n".format(self._block_size*self._word_size + 4)
        asm_valid = "valid:\n\taddi x31, x0, 1\n"
        asm_end = "end:\n\tnop\n\tfence.i\n"
        

	    asm = asm_main + asm_pass1 + asm_pass2 + asm_pass3 + asm_pass4 + asm_pass5 + asm_pass6 + asm_pass7 + asm_pass8 + asm_pass9 + asm_pass10 + asm_pass11 + asm_pass12 + asm_valid + asm_end
        compile_macros = []    	
    	
    	return [{
            'asm_code': asm,
            'asm_sig': '',
            'compile_macros': compile_macros
        }]