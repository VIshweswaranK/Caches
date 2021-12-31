# Caches

This repository contains the python scripts to generate RISC-V Assembly for testing the [Cache subsystem](https://gitlab.com/incoresemi/blocks/cache_subsystem/-/tree/master/) in the Chromite Core by [InCore Semiconductors](https://incoresemi.com/).

A [Data Caches](https://gitlab.com/incoresemi/blocks/cache_subsystem/-/blob/1r1w-dcache-instance/src/dcache/dcache1r1w.bsv) and [Instruction Caches](https://gitlab.com/incoresemi/blocks/cache_subsystem/-/blob/1r1w-dcache-instance/src/icache/icache.bsv) are developed as modules by [InCore Semiconductors](https://incoresemi.com/).

A rough explaination of the Caches is given [here](https://chromite.readthedocs.io/en/using-csrbox/cache.html).

This repository can be initialised as a submodule in [chromite_uatg_tests](https://github.com/incoresemi/chromite_uatg_tests).

## File Structure

```text
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

## Test Description

- Fill the cache completely based on the size mentioned in the core64.yaml input.
- Try to fill the fill-buffer completely.
- Perform cache line thrashing
- Perform cache set thrashing
- Perform all possible types of load/store access (byte, hword, word, dword)
- Perform a load/store hit in the RAMS
- Perform a load/store hit in the Fill-buffer
- Perform an I/O operation
- Perform a store-to-load forwarding scenario from the store-buffer
- Perform a replacement on all sets.
- Check if fence and fence.iwork properly
- Check if performance counters are correctly incremented.
- Check to see if we can perform simultaneous io and cached ops

## Code Description

### dcache_fill_01.py

- Perform a `fence` operation to clear out the data cache subsystem and the fill buffer.
- Load some data into a temporary register and perform `numerous store operations` to fill up the cache.
- Each loop in ASM has an unconditional `jump` back to that label, a branch takes us out of the loop.
- Each iteration, we visit the next `set`.
- The total number of iterations is parameterized based on YAML input.

### dcache_fill_02.py

- Perform a `fence` operation to clear out the data cache subsystem and the fill buffer.
- In each iteration, we visit the next way in the same set. Once all the ways in a set are touched, we visit the next set.
- The total number of iterations is parameterized based on YAML input.

### dcache_fill_03.py

- Perform a `fence` operation to clear out the data cache subsystem and the fill buffer.
- Perform `numerous load operations` to fill up the cache
- In each iteration, we visit the next way in the same set. Once all the ways in a set are touched, we visit the next set.
- The total number of iterations is parameterized based on YAML input.

### dcache_fill_04.py

- Perform a `fence` operation to clear out the data cache subsystem and the fill buffer.
- Load some data into a temporary register and perform `numerous load operations` to fill up the cache.
- Each loop in ASM has an unconditional `jump` back to that label, a branch takes us out of the loop.
- Each iteration, we visit the next `set`.
- The total number of iterations is parameterized based on YAML input.

### dcache_fill_buffer_01.py

- Perform a `fence` operation to clear out the data cache subsystem and the fill buffer.
- Load some data into a temporary register and perform `numerous store operations` to fill up the cache.
- Each loop in ASM has an unconditional `jump` back to that label, a branch takes us out of the loop.
- Each iteration, we visit the next `set`.
- The total number of iterations is parameterized based on YAML input.
- Once the cache is full, we perform numerous `consecutive store operations`.
- The number of iterations is parameterized based on the YAML input such that the fill_buffer is completely full.
- Post filling the caches, we perform a series of `nop` instructions to ensure that the fill buffer is empty.

### dcache_fill_buffer_02.py

- Perform a `fence` operation to clear out the data cache subsystem and the fill buffer.
- Perform `numerous load operations` to fill up the cache
- In each iteration, we visit the next way in the same set. Once all the ways in a set are touched, we visit the next set.
- The total number of iterations is parameterized based on YAML input.
- Once the cache is full, we perform numerous `consecutive load operations`.
- The number of iterations is parameterized based on the YAML input such that the fill_buffer is completely full.
- Post filling the caches, we perform a series of `nop` instructions to ensure that the fill buffer is empty.

### dcache_line_thrashing.py

- Perform a  `fence`  operation to clear out the data cache subsystem and the fill buffer.
- First the cache is filled up using the following logic. For an *n-way* cache system, in each set there is *only 1 non dirty way* and the remaining *n-1 ways are dirty*.
- Now a series of `nop` operations are done inorder the ensure that the fillbuffer is empty and the cache is completely full.
- This is followed by a large series of back to back `store operations` with an address that maps to a single set in the cache. This ensures that the fillbuffer gets filled and the line thrashing process begins.
- Now after the fill buffer is full, with each store operation a cache miss is encountered and the non-dirty line in the set will be replaced.
- This process is iterated to test each cache line

### dcache_set_thrashing.py

- Perform a  `fence`  operation to clear out the data cache subsystem and the fill buffer.
- First the cache is filled up using the following logic. All the ways of a set should either be  *dirty or clean*.
- This is followed by a large series of back to back `store operations` with an address that maps to a single set in the cache. This ensures that the fillbuffer gets filled and the line thrashing process begins.
- Now after the fill buffer is full, with each store operation a cache miss is encountered and the non-dirty line in the set will be replaced.
- This process is iterated to test each cache line

## Initializing test data

- Initialise `rvtest_data` with some random values as follows:
     For the size of `(block_size * sets * ways)`, we do the following:
    `asm_data +=  "\t.word 0x{0:08x}\n".format(random.randrange(16**8)`

## Code Generation using UATG

```text
    INFO | ****** Micro-Architectural Test Generator - UATG *******
    INFO | Version : 1.3.0
    INFO | Copyright (c) 2021, InCore Semiconductors Pvt. Ltd.
    INFO | All Rights Reserved.
    INFO | uatg dir is /home/bkkarthik/miniconda3/envs/chromite3.7/lib/python3.7/site-packages/uatg
    INFO | work_dir is /home/bkkarthik/incore/pre/chromite-core-verif/mywork/
   DEBUG | The modules are Caches
    INFO | ****** Generating Tests ******
   DEBUG | Directory for Caches is /home/bkkarthik/incore/pre/chromite_uatg_tests/modules/Caches
    INFO | Starting plugin Creation for Caches
   DEBUG | Created plugin for uatg_cache_dcache_load_store_op
   DEBUG | Created plugin for uatg_cache_dcache_fill_02
   DEBUG | Created plugin for uatg_cache_dcache_fill_03
   DEBUG | Created plugin for uatg_cache_dcache_fill_buffer_01
   DEBUG | Created plugin for uatg_cache_dcache_set_thrashing
   DEBUG | Created plugin for uatg_cache_dcache_fill_01
   DEBUG | Created plugin for uatg_cache_dcache_fill_buffer_02
   DEBUG | Created plugin for uatg_cache_dcache_line_thrashing
   DEBUG | Created plugin for uatg_cache_dcache_fill_04
    INFO | Created plugins for Caches
   DEBUG | Generating assembly tests for Caches
   DEBUG | Selected test: uatg_cache_dcache_fill_04-001
   DEBUG | Generating test for uatg_cache_dcache_fill_04-001
   DEBUG | Finished Generating Assembly Files for uatg_cache_dcache_fill_04
   DEBUG | Selected test: uatg_cache_dcache_line_thrashing-001
   DEBUG | Generating test for uatg_cache_dcache_line_thrashing-001
   DEBUG | Finished Generating Assembly Files for uatg_cache_dcache_line_thrashing
   DEBUG | Selected test: uatg_cache_dcache_fill_03-001
   DEBUG | Generating test for uatg_cache_dcache_fill_03-001
   DEBUG | Finished Generating Assembly Files for uatg_cache_dcache_fill_03
   DEBUG | Selected test: uatg_cache_dcache_load_store_op-001
   DEBUG | Selected test: uatg_cache_dcache_fill_buffer_01-001
   DEBUG | Generating test for uatg_cache_dcache_load_store_op-001
   DEBUG | Generating test for uatg_cache_dcache_fill_buffer_01-001
   DEBUG | Selected test: uatg_cache_dcache_fill_01-001
   DEBUG | Generating test for uatg_cache_dcache_fill_01-001
   DEBUG | Finished Generating Assembly Files for uatg_cache_dcache_load_store_op
   DEBUG | Finished Generating Assembly Files for uatg_cache_dcache_fill_buffer_01
   DEBUG | Finished Generating Assembly Files for uatg_cache_dcache_fill_01
   DEBUG | Selected test: uatg_cache_dcache_fill_buffer_02-001
   DEBUG | Selected test: uatg_cache_dcache_set_thrashing-001
   DEBUG | Generating test for uatg_cache_dcache_set_thrashing-001
   DEBUG | Generating test for uatg_cache_dcache_fill_buffer_02-001
   DEBUG | Finished Generating Assembly Files for uatg_cache_dcache_set_thrashing
   DEBUG | Finished Generating Assembly Files for uatg_cache_dcache_fill_buffer_02
   DEBUG | Selected test: uatg_cache_dcache_fill_02-001
   DEBUG | Generating test for uatg_cache_dcache_fill_02-001
   DEBUG | Finished Generating Assembly Files for uatg_cache_dcache_fill_02
   DEBUG | Finished Generating Assembly Tests for Caches
    INFO | Creating test_list for the Caches
   DEBUG | Current test is /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_fill_buffer_02-001/uatg_cache_dcache_fill_buffer_02-001.S
   DEBUG | Current test is /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_set_thrashing-001/uatg_cache_dcache_set_thrashing-001.S
   DEBUG | Current test is /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_fill_03-001/uatg_cache_dcache_fill_03-001.S
   DEBUG | Current test is /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_load_store_op-001/uatg_cache_dcache_load_store_op-001.S
   DEBUG | Current test is /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_fill_buffer_01-001/uatg_cache_dcache_fill_buffer_01-001.S
   DEBUG | Current test is /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_line_thrashing-001/uatg_cache_dcache_line_thrashing-001.S
   DEBUG | Current test is /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_fill_02-001/uatg_cache_dcache_fill_02-001.S
   DEBUG | Current test is /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_fill_04-001/uatg_cache_dcache_fill_04-001.S
   DEBUG | Current test is /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_fill_01-001/uatg_cache_dcache_fill_01-001.S
   DEBUG | Dumping makefile
    INFO | ****** Finished Generating Tests ******
   DEBUG | Using user specified linker: /home/bkkarthik/incore/pre/chromite_uatg_tests/target/link.ld
   DEBUG | Using user specified model_test file: /home/bkkarthik/incore/pre/chromite_uatg_tests/target/model_test.h
    INFO | Test List was generated by UATG. You can find it in the work dir 

```

## Compile Testing the ASM generated using UATG

```bash
$ make uatg_cache_dcache_fill_01-001 
riscv64-unknown-elf-gcc -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf -fvisibility=hidden -static -nostdlib -nostartfiles -lm -lgcc -march=rv64imac -mabi=lp64 -lm -lgcc -T /home/bkkarthik/incore/pre/chromite_uatg_tests/target/link.ld /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_fill_01-001/uatg_cache_dcache_fill_01-001.S -I /home/bkkarthik/miniconda3/envs/chromite3.7/lib/python3.7/site-packages/uatg/env -I /home/bkkarthik/incore/pre/chromite-core-verif/mywork/ -DXLEN=64 -o /dev/null
$ make uatg_cache_dcache_fill_02-001 
riscv64-unknown-elf-gcc -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf -fvisibility=hidden -static -nostdlib -nostartfiles -lm -lgcc -march=rv64imac -mabi=lp64 -lm -lgcc -T /home/bkkarthik/incore/pre/chromite_uatg_tests/target/link.ld /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_fill_02-001/uatg_cache_dcache_fill_02-001.S -I /home/bkkarthik/miniconda3/envs/chromite3.7/lib/python3.7/site-packages/uatg/env -I /home/bkkarthik/incore/pre/chromite-core-verif/mywork/ -DXLEN=64 -o /dev/null
$ make uatg_cache_dcache_fill_03-001 
riscv64-unknown-elf-gcc -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf -fvisibility=hidden -static -nostdlib -nostartfiles -lm -lgcc -march=rv64imac -mabi=lp64 -lm -lgcc -T /home/bkkarthik/incore/pre/chromite_uatg_tests/target/link.ld /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_fill_03-001/uatg_cache_dcache_fill_03-001.S -I /home/bkkarthik/miniconda3/envs/chromite3.7/lib/python3.7/site-packages/uatg/env -I /home/bkkarthik/incore/pre/chromite-core-verif/mywork/ -DXLEN=64 -o /dev/null
$ make uatg_cache_dcache_fill_04-001 
riscv64-unknown-elf-gcc -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf -fvisibility=hidden -static -nostdlib -nostartfiles -lm -lgcc -march=rv64imac -mabi=lp64 -lm -lgcc -T /home/bkkarthik/incore/pre/chromite_uatg_tests/target/link.ld /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_fill_04-001/uatg_cache_dcache_fill_04-001.S -I /home/bkkarthik/miniconda3/envs/chromite3.7/lib/python3.7/site-packages/uatg/env -I /home/bkkarthik/incore/pre/chromite-core-verif/mywork/ -DXLEN=64 -o /dev/null
$ make uatg_cache_dcache_fill_buffer_01-001 
riscv64-unknown-elf-gcc -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf -fvisibility=hidden -static -nostdlib -nostartfiles -lm -lgcc -march=rv64imac -mabi=lp64 -lm -lgcc -T /home/bkkarthik/incore/pre/chromite_uatg_tests/target/link.ld /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_fill_buffer_01-001/uatg_cache_dcache_fill_buffer_01-001.S -I /home/bkkarthik/miniconda3/envs/chromite3.7/lib/python3.7/site-packages/uatg/env -I /home/bkkarthik/incore/pre/chromite-core-verif/mywork/ -DXLEN=64 -o /dev/null
$ make uatg_cache_dcache_fill_buffer_02-001 
riscv64-unknown-elf-gcc -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf -fvisibility=hidden -static -nostdlib -nostartfiles -lm -lgcc -march=rv64imac -mabi=lp64 -lm -lgcc -T /home/bkkarthik/incore/pre/chromite_uatg_tests/target/link.ld /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_fill_buffer_02-001/uatg_cache_dcache_fill_buffer_02-001.S -I /home/bkkarthik/miniconda3/envs/chromite3.7/lib/python3.7/site-packages/uatg/env -I /home/bkkarthik/incore/pre/chromite-core-verif/mywork/ -DXLEN=64 -o /dev/null
$ make uatg_cache_dcache_line_thrashing-001
riscv64-unknown-elf-gcc -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf -fvisibility=hidden -static -nostdlib -nostartfiles -lm -lgcc -march=rv64imac -mabi=lp64 -lm -lgcc -T /home/bkkarthik/incore/pre/chromite_uatg_tests/target/link.ld /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_line_thrashing-001/uatg_cache_dcache_line_thrashing-001.S -I /home/bkkarthik/miniconda3/envs/chromite3.7/lib/python3.7/site-packages/uatg/env -I /home/bkkarthik/incore/pre/chromite-core-verif/mywork/ -DXLEN=64 -o /dev/null
$ make uatg_cache_dcache_set_thrashing-001
riscv64-unknown-elf-gcc -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf -fvisibility=hidden -static -nostdlib -nostartfiles -lm -lgcc -march=rv64imac -mabi=lp64 -lm -lgcc -T /home/bkkarthik/incore/pre/chromite_uatg_tests/target/link.ld /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_set_thrashing-001/uatg_cache_dcache_set_thrashing-001.S -I /home/bkkarthik/miniconda3/envs/chromite3.7/lib/python3.7/site-packages/uatg/env -I /home/bkkarthik/incore/pre/chromite-core-verif/mywork/ -DXLEN=64 -o /dev/null
$ make uatg_cache_dcache_load_store_op-001
riscv64-unknown-elf-gcc -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf -fvisibility=hidden -static -nostdlib -nostartfiles -lm -lgcc -march=rv64imac -mabi=lp64 -lm -lgcc -T /home/bkkarthik/incore/pre/chromite_uatg_tests/target/link.ld /home/bkkarthik/incore/pre/chromite-core-verif/mywork/Caches/uatg_cache_dcache_load_store_op-001/uatg_cache_dcache_load_store_op-001.S -I /home/bkkarthik/miniconda3/envs/chromite3.7/lib/python3.7/site-packages/uatg/env -I /home/bkkarthik/incore/pre/chromite-core-verif/mywork/ -DXLEN=64 -o /dev/null
$ 
```

## Contributors

Vishweshwaran K <<vishwa.kans07@gmail.com>>,
Karthik B K <<bkkarthik@pesu.pes.edu>>
