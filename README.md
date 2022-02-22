# RISC-V Function Profiling from Waveforms

This project implements a function-level RISC-V profiler that extracts the time spent in each function out of a simulation waveform.
The profiler program consists of a single Python script that accesses and analyzes the waveform data using the [Waveform Analysis Language](https://github.com/ics-jku/wal). It is not tied to any particular RISC-V core and can be easily adapted to new cores over a single configuration file.


## Installation
The only reuirement for this script is Python < 3.10 and the *wal-lang* Python package.
Install WAL by typing `pip install wal-lang`.

_On some systems, pip does not add WALs installation path to the PATH variable. If the "wal" command is not available after installation please add the installation path, e.g. ~/.local/bin on Ubuntu, to your PATH variable._

## Profiling Waveforms
To profile a waveform you need to have a RISC-V elf binary and a vcd waveform of a RISC-V core running the binary.
Profiling is started py running the Python script with the elf file as the first and the vcd file as the second argument.

This repository contains examples for the SERV and VexRiscv cores.
Tue to space concerns I have converted the larger vcd files to the fst format. However, currently WAL only supports vcd files therefore you have to 
convert the fst files back to vcd using the "fst2vcd" command included with gtkwave. 

If you dont have gtkwave installed you can still try the vexriscv/gcd example!

### SERV
A bubblesort implementation sorting an array of 20 integers. Supplemented with additional printing and memcpy functions.
```
cd serv;
fst2vcd bubblesort.fst > bubblesort.vcd;
../profile.py bubblesort.elf bubblesort.vcd
```

### VexRiscv
A simple example with a greates common divisor implementation.
```
cd vexriscv;
../profile.py gcd.elf gcd.vcd
```

The Dhrystone benchmark running on the VexRiscv.
```
cd vexriscv;
fst2vcd dhrystone.fst > dhrystone.vcd;
../profile.py dhrystone.elf dhrystone.vcd
```

## How does it work?
This program extracts information about the functions from the elf file using the "nm" command. This command prints a list of all symbols and their sizes*.
Using this information the start and end addresses of functions is calculated. Then, the WAL code, which is embedded into the main script similar to SQL query, searches the waveform for all executed instructions and their location in the binary. The location is then compared to the function address ranges and a counter for the function that is associated to this address is incremented.

### Adapting to Other Cores
To adapted a new core to this script is easy. All you have to do is to know the name of the clk signal, detect when an instruction is commited and which address this instruction had.
This information can than be entered in a new `config.wal` file just like the ones in [SERV](https://github.com/LucasKl/riscv-function-profiling/blob/main/serv/config.wal) and [VexRiscv](https://github.com/LucasKl/riscv-function-profiling/blob/main/vexriscv/config.wal) config files.

The config file specifies three alternative names at which the WAL program finds the information it needs.

```
(alias clk TOP.servant_sim.dut.cpu.clk)
(alias fire TOP.servant_sim.dut.wb_ibus_ack)
(alias pc TOP.servant_sim.dut.wb_ibus_adr)
```

So you have to change `(alias clk ....)` to `(alias clk you.clk.signal)`
