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

## Code Description

#### dcache_fill_01.py
- Perform a `fence` operation to clear out the data cache subsystem and the fill buffer. 
- Load some data into a temporary register and perform `numerous store operations` to fill up the cache.
- Each loop in ASM has an unconditional `jump` back to that label, a branch takes us out of the loop.
- Each iteration, we visit the next `set`.
- The total number of iterations is parameterized based on YAML input.
#### dcache_fill_02.py
- Perform a `fence` operation to clear out the data cache subsystem and the fill buffer. 
- In each iteration, we visit the next way in the same set. Once all the ways in a set are touched, we visit the next set.
- The total number of iterations is parameterized based on YAML input.
#### dcache_fill_03.py
-  Perform a `fence` operation to clear out the data cache subsystem and the fill buffer. 
- Perform `numerous load operations` to fill up the cache
- In each iteration, we visit the next way in the same set. Once all the ways in a set are touched, we visit the next set.
- The total number of iterations is parameterized based on YAML input.
#### dcache_fill_04.py
- Perform a `fence` operation to clear out the data cache subsystem and the fill buffer. 
- Load some data into a temporary register and perform `numerous load operations` to fill up the cache.
- Each loop in ASM has an unconditional `jump` back to that label, a branch takes us out of the loop.
- Each iteration, we visit the next `set`.
- The total number of iterations is parameterized based on YAML input.
## Initializing test data
- Initialise `rvtest_data` with some random values as follows:
     `for  i  in  range (self._block_size  *  self._sets  *  self._ways):`
    `asm_data +=  "\t.word 0x{0:08x}\n".format(random.randrange(16**8)`