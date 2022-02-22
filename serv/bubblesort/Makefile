elf:
	$(RISCV_PREFIX)gcc -nostartfiles -nostdlib -march=rv32i -mabi=ilp32 -Tlink.ld bootstrap.S main.c -o bubblesort.elf
bin: elf
	$(RISCV_PREFIX)objcopy -O binary bubblesort.elf bubblesort.bin
hex: bin
	python3 makehex.py bubblesort.bin 2048 > bubblesort.hex

clean:
	rm -f *.elf *.bin *.hex
