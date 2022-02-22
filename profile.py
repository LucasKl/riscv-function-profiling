from wal.core import Wal
import sys
import os
import subprocess

def ranges(binary_file):
    '''This functions extracts the functions from elf files using "nm"'''
    res = []

    proc = subprocess.Popen( [ os.environ['RISCV_PREFIX'] + 'nm' , '-S', binary_file], stdout=subprocess.PIPE )
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

    if 'RISCV_PREFIX' not in os.environ:
        print('Please add RISCV_PREFIX to you path')
        exit(1)

    BIN = sys.argv[1]
    VCD = sys.argv[2]

    functions = ranges(BIN)

    wal = Wal()
    wal.load(VCD)
    wal.eval('(require config)') # require config script to get concrete signal names        
    wal.eval('''(defun count-function [addr]
                  (for [f funcs]
                    (when (&& (>= addr f[1]) (<= addr f[2]))
    	              (seta dist f[0] (+ (geta/default dist 0 f[0]) 1)))))''')

    # calculate the time spent in each function, does not take subcalls into account
    dist = {}
    wal.eval('(whenever (&& clk fire) (count-function pc))', funcs=functions, dist=dist)
    # get number of executed instructions
    instructions_executed = wal.eval('(length (find (&& clk fire)))')

    # print results
    print('Time spent in functions:')
    for name, count in dist.items():
        print(f'{name:>10}: {count/instructions_executed*100:.2f}% ({count})')
