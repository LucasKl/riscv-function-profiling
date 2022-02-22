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


