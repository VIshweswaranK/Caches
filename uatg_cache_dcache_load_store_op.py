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
    	asm_main = "li t1, 8000\n\tli t2, 1718000025\n\tli a2, 153\n\tsb t2, 32(t1)\n\tlbu t3, 32(t1)\n\tbne a2, t3, false\n"
        asm_pass1 = "pass1:\n\tli a2, 39321\n\tsh t2, 64(t1)\n\tlhu t3, 64(t1)\n\tbne a2, t3, false\n"
        asm_pass2 = "pass2:\n\tli a2, 1718000025\n\tsw t2, 96(t1)\n\tlwu t3, 96(t1)\n\tbne a2, t3, false\n"
        asm_pass3 = "pass3:\n\tli a2, 4294967193\n\tlb t3, 32(t1)\n\tbne t3, a2, false\n"
        asm_pass4 = "pass4:\n\tli a2, 4294941081\n\tlh t3, 64(t1)\n\tbne t3, a2, false\n"
        asm_pass5 = "pass5:\n\tli a2, 1718000025\n\tlw t3, 96(t1)\n\tbne t3, a2, false\n\tj end\n"
        asm_false = "false:\n\tli x30, 1\n"
        asm_end = "end:\n\tnop\n"

	    asm = asm_main + asm_pass1 + asm_pass2 + asm_pass3 + asm_pass4 + asm_pass5 + asm_false + asm_end
        compile_macros = []    	
    	
    	return [{
            'asm_code': asm,
            'asm_sig': '',
            'compile_macros': compile_macros
        }]