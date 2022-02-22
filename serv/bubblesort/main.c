#include <stdint.h>
#include <stddef.h>

static volatile int * const PRINT_CHAR_ADDR = (int * const)1024;
static volatile int * const PRINT_INT_ADDR = (int * const)1016;


void *memcpy(void *dest, const void *src, size_t n) {
    for (size_t i = 0; i < n; i++) {
        ((char*)dest)[i] = ((char*)src)[i];
    }
}

void print(int* data, unsigned int size) {
    for (int i = 0; i != size; i++) {
      *PRINT_INT_ADDR = data[i];
      *PRINT_CHAR_ADDR = ' ';
    }
    *PRINT_CHAR_ADDR = '\n';
}

void sort(int* data, unsigned int size) {
  int swapped = 1;

  while (swapped) {
    print(data, size);
    swapped = 0;
    for (int i = 1; i != size; i++) {
      if (data[i] <= data[i-1]) {
	int tmp = data[i-1];
	data[i-1] = data[i];
	data[i] = tmp;
	if (data[i] != data[i-1]) swapped = 1;
      }
    }
  }

  print(data, size);
}

int main() {

  int test_0[20] = {58, 37, 38, 4, 81, 61, 30, 83, 3, 87, 58, 37, 38, 4, 81, 61, 30, 83, 3, 87 };
  int test_0_size = 20;
  sort(test_0, test_0_size);


  
  return 0;
}
