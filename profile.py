#!/bin/python
from wal.core import Wal
import sys
import os
import subprocess

def ranges(binary_file):
    '''This functions extracts the functions from elf files using "nm"'''
    res = []

    if 'RISCV_PREFIX' in os.environ:
        proc = subprocess.Popen( [ os.environ['RISCV_PREFIX'] + 'nm' , '-S', binary_file], stdout=subprocess.PIPE )
    else:
        print('Please add the location of you RISC-V toolchain to the "RISCV_PREFIX" variable.')
        print('Now trying to fall back to the regular "nm"..\n')
        try:
            proc = subprocess.Popen( [ 'nm' , '-S', binary_file], stdout=subprocess.PIPE )
        except:
            print('"nm" not found on system')
            exit(1)
        
    stdout, _ = proc.communicate()
    symbols = stdout.decode('UTF-8')

    print(f'Functions in "{binary_file}"')
    for line in symbols.split('\n'):
        cols = line.split()
        if len(cols) == 4 and cols[2] == 'T':
            name = cols[3]
            start = int(cols[0], 16)
            end = start + int(cols[1], 16) - 4
            print(f'{name:>20} {start:x}-{end:x}')
            res.append([name, start, end, 0])

    print('\n')
    return res


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage:')
        print('  profile.py elf vcd')
        exit(1)

    BIN = sys.argv[1]
    VCD = sys.argv[2]

    functions = ranges(BIN)

    wal = Wal()
    wal.load(VCD)
    wal.eval_str('(eval-file config)') # require config script to get concrete signal names

    def count_function(seval, addr):
        addr = seval.eval(addr[0])
        for function in functions:
            if addr >= function[1] and addr <= function[2]:
                function[3] += 1
                return

    wal.register_operator("count-function", count_function)

    # calculate the time spent in each function, does not take subcalls into account
    wal.eval_str('(define ninstr 0)')
    instructions_executed = wal.eval_str('(whenever (fire) (count-function pc) (inc ninstr))', funcs=functions)

    # print results
    in_known_function = 0
    print('Time spent in functions:')
    for function in functions:
        name = function[0]
        count = function[3]
        in_known_function += count
        print(f'{name:>20}: {count/instructions_executed*100:.2f}% ({count})')

    print(f'{"other":>20}: {(instructions_executed - in_known_function)/instructions_executed*100:.2f}% ({instructions_executed - in_known_function})')
