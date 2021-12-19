# Caches
This repository contains the python scripts to generate RISC-V Assembly for testing the Cache subsystem in the Chromite Core by InCore Semiconductors.

This repository can be initialised as a submodule in [chromite_uatg_tests](https://github.com/incoresemi/chromite_uatg_tests).

## File Structure
```
.
├── README.md -- Describes the idea behind each test and how the ASM is generated efficiently using Python 3.
├── uatg_cache_dcache_fill_01.py -- Generates ASM to fill the Data Cache by performing consecutive stores at different address locations, jumps to the next set in each iteration.
├── uatg_cache_dcache_fill_02.py -- Generates ASM to fill the Data Cache by performing consecutive stores at different address locations, jumps to the next line in each iteration.
├── uatg_cache_dcache_fill_03.py -- Generates ASM to fill the Data Cache by performing consecutive loads at different address locations, jumps to the next set in each iteration.
├── uatg_cache_dcache_fill_04.py -- Generates ASM to fill the Data Cache by performing consecutive loads at different address locations, jumps to the next line in each iteration.
├── uatg_cache_dcache_fill_buffer_01.py -- Generates ASM to fill the Fill Buffer post filling the Data Cache completely. Performs consecutive stores.
├── uatg_cache_dcache_fill_buffer_02.py -- Generates ASM to fill the Fill Buffer post filling the Data Cache completely. Performs consecutive loads.
├── uatg_cache_dcache_line_thrashing.py -- Generates ASM to perform Cache Line Thrashing.
├── uatg_cache_dcache_load_store_op.py -- Generates ASM to perform all types of load and store operations.
└── uatg_cache_dcache_set_thrashing.py -- Generates ASM to perform Cache Set Thrashing.
```

## Contributors
Vishweshwaran K <<vishwa.kans07@gmail.com>>,
Karthik B K <<bkkarthik@pesu.pes.edu>>
