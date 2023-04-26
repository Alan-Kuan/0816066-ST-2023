# Software Testing: Lab06
0816066 官澔恩

## Environment
- Linux Kernel: 6.2.11-zen1-1-zen
- GCC: 12.2.1
- Valgrind: 3.20.0

## Experiment 1
### Summary

| | Valgrind | ASan |
| --- | :---: | :---: |
| Heap Out-of-bound | :heavy_check_mark: | :heavy_check_mark: |
| Stack Out-of-bound | :x: | :heavy_check_mark: |
| Global Out-of-bound | :x: | :heavy_check_mark: |
| Use-after-free | :heavy_check_mark: | :heavy_check_mark: |
| Use-after-return | :x: | :heavy_check_mark: |

### 1. Heap Out-of-bound
#### Malfunction Code
**[** heap-oob.c **]**:
```c
#include <stdlib.h>

int main(void) {
    int* a = (int*) malloc(4 * sizeof(int));
    a[5] = 1;
    free(a);
    return 0;
}
```

#### Valgrind Report
```sh
$ gcc ./heap-oob.c -o heap-oob
$ valgrind ./heap-oob
```

```
==3445460== Memcheck, a memory error detector
==3445460== Copyright (C) 2002-2022, and GNU GPL'd, by Julian Seward et al.
==3445460== Using Valgrind-3.20.0 and LibVEX; rerun with -h for copyright info
==3445460== Command: ./heap-oob
==3445460==
==3445460== Invalid write of size 4
==3445460==    at 0x109167: main (in /home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/heap-oob)
==3445460==  Address 0x4a6d054 is 4 bytes after a block of size 16 alloc'd
==3445460==    at 0x4841888: malloc (vg_replace_malloc.c:393)
==3445460==    by 0x10915A: main (in /home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/heap-oob)
==3445460==
==3445460==
==3445460== HEAP SUMMARY:
==3445460==     in use at exit: 0 bytes in 0 blocks
==3445460==   total heap usage: 1 allocs, 1 frees, 16 bytes allocated
==3445460==
==3445460== All heap blocks were freed -- no leaks are possible
==3445460==
==3445460== For lists of detected and suppressed errors, rerun with: -s
==3445460== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

#### ASan Report
```sh
$ gcc ./heap-oob.c -fsanitize=address -o heap-oob
$ ./heap-oob
```

```
=================================================================
==3449554==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000024 at pc 0x561a801c41ce bp 0x7ffd3ed63c40 sp 0x7ffd3ed63c30
WRITE of size 4 at 0x602000000024 thread T0
    #0 0x561a801c41cd in main (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/heap-oob+0x11cd)
    #1 0x7fb57663c78f  (/usr/lib/libc.so.6+0x2378f)
    #2 0x7fb57663c849 in __libc_start_main (/usr/lib/libc.so.6+0x23849)
    #3 0x561a801c40a4 in _start (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/heap-oob+0x10a4)

0x602000000024 is located 4 bytes to the right of 16-byte region [0x602000000010,0x602000000020)
allocated by thread T0 here:
    #0 0x7fb5768bfa89 in __interceptor_malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x561a801c418a in main (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/heap-oob+0x118a)
    #2 0x7fb57663c78f  (/usr/lib/libc.so.6+0x2378f)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/heap-oob+0x11cd) in main
Shadow bytes around the buggy address:
  0x0c047fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c047fff8000: fa fa 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==3449554==ABORTING
```

Both Valgrind and ASan detected the error.

### 2. Stack Out-of-bound
#### Malfunction Code
**[** stack-oob.c **]**:
```c
int main(void) {
    int a[4];
    a[5] = 1;
    return 0;
}
```

#### Valgrind Report
```sh
$ gcc ./stack-oob.c -o stack-oob
$ valgrind ./stack-oob
```

```
==3447073== Memcheck, a memory error detector
==3447073== Copyright (C) 2002-2022, and GNU GPL'd, by Julian Seward et al.
==3447073== Using Valgrind-3.20.0 and LibVEX; rerun with -h for copyright info
==3447073== Command: ./stack-oob
==3447073==
==3447073==
==3447073== HEAP SUMMARY:
==3447073==     in use at exit: 0 bytes in 0 blocks
==3447073==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==3447073==
==3447073== All heap blocks were freed -- no leaks are possible
==3447073==
==3447073== For lists of detected and suppressed errors, rerun with: -s
==3447073== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

#### ASan Report
```sh
$ gcc ./stack-oob.c -fsanitize=address -o stack-oob
$ ./stack-oob
```

```
=================================================================
==3450193==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffc6b22cc04 at pc 0x55f0998c2231 bp 0x7ffc6b22cbc0 sp 0x7ffc6b22cbb0
WRITE of size 4 at 0x7ffc6b22cc04 thread T0
    #0 0x55f0998c2230 in main (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/stack-oob+0x1230)
    #1 0x7f3fc883c78f  (/usr/lib/libc.so.6+0x2378f)
    #2 0x7f3fc883c849 in __libc_start_main (/usr/lib/libc.so.6+0x23849)
    #3 0x55f0998c20a4 in _start (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/stack-oob+0x10a4)

Address 0x7ffc6b22cc04 is located in stack of thread T0 at offset 52 in frame
    #0 0x55f0998c2188 in main (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/stack-oob+0x1188)

  This frame has 1 object(s):
    [32, 48) 'a' (line 2) <== Memory access at offset 52 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/stack-oob+0x1230) in main
Shadow bytes around the buggy address:
  0x10000d63d930: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10000d63d940: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10000d63d950: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10000d63d960: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10000d63d970: 00 00 00 00 00 00 00 00 00 00 f1 f1 f1 f1 00 00
=>0x10000d63d980:[f3]f3 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10000d63d990: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10000d63d9a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10000d63d9b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10000d63d9c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10000d63d9d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==3450193==ABORTING
```

Only ASan detected the error.

### 3. Global Out-of-bound
#### Malfunction Code
**[** global-oob.c **]**:
```c
int a[4];

int main(void) {
    a[5] = 1;
    return 0;
}
```

#### Valgrind Report
```sh
$ gcc ./global-oob.c -o global-oob
$ valgrind ./global-oob
```

```
==3459337== Memcheck, a memory error detector
==3459337== Copyright (C) 2002-2022, and GNU GPL'd, by Julian Seward et al.
==3459337== Using Valgrind-3.20.0 and LibVEX; rerun with -h for copyright info
==3459337== Command: ./global-oob
==3459337==
==3459337==
==3459337== HEAP SUMMARY:
==3459337==     in use at exit: 0 bytes in 0 blocks
==3459337==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==3459337==
==3459337== All heap blocks were freed -- no leaks are possible
==3459337==
==3459337== For lists of detected and suppressed errors, rerun with: -s
==3459337== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

#### ASan Report
```sh
$ gcc ./global-oob.c -fsanitize=address -o global-oob
$ ./global-oob
```

```
=================================================================
==3459992==ERROR: AddressSanitizer: global-buffer-overflow on address 0x56451c7200f4 at pc 0x56451c71d1b7 bp 0x7ffdece64a20 sp 0x7ffdece64a10
WRITE of size 4 at 0x56451c7200f4 thread T0
    #0 0x56451c71d1b6 in main (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/global-oob+0x11b6)
    #1 0x7fa8ec43c78f  (/usr/lib/libc.so.6+0x2378f)
    #2 0x7fa8ec43c849 in __libc_start_main (/usr/lib/libc.so.6+0x23849)
    #3 0x56451c71d0a4 in _start (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/global-oob+0x10a4)

0x56451c7200f4 is located 4 bytes to the right of global variable 'a' defined in 'global-oob.c:1:5' (0x56451c7200e0) of size 16
SUMMARY: AddressSanitizer: global-buffer-overflow (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/global-oob+0x11b6) in main
Shadow bytes around the buggy address:
  0x0ac9238dbfc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac9238dbfd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac9238dbfe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac9238dbff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac9238dc000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0ac9238dc010: f9 f9 f9 f9 f9 f9 f9 f9 00 00 00 00 00 00[f9]f9
  0x0ac9238dc020: f9 f9 f9 f9 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac9238dc030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac9238dc040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac9238dc050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac9238dc060: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==3459992==ABORTING
```

Only ASan detected the error.

### 4. Use-after-free
#### Malfunction Code
**[** use-after-free.c **]**:
```c
#include <stdlib.h>

int main(void) {
    int* a = (int*) malloc(sizeof(int));
    free(a);
    *a = 1;
    return 0;
}
```

#### Valgrind Report
```sh
$ gcc ./use-after-free.c -o use-after-free
$ valgrind ./use-after-free
```

```
==3453750== Memcheck, a memory error detector
==3453750== Copyright (C) 2002-2022, and GNU GPL'd, by Julian Seward et al.
==3453750== Using Valgrind-3.20.0 and LibVEX; rerun with -h for copyright info
==3453750== Command: ./use-after-free
==3453750==
==3453750== Invalid write of size 4
==3453750==    at 0x10916F: main (in /home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/use-after-free)
==3453750==  Address 0x4a6d040 is 0 bytes inside a block of size 4 free'd
==3453750==    at 0x484426F: free (vg_replace_malloc.c:884)
==3453750==    by 0x10916A: main (in /home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/use-after-free)
==3453750==  Block was alloc'd at
==3453750==    at 0x4841888: malloc (vg_replace_malloc.c:393)
==3453750==    by 0x10915A: main (in /home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/use-after-free)
==3453750==
==3453750==
==3453750== HEAP SUMMARY:
==3453750==     in use at exit: 0 bytes in 0 blocks
==3453750==   total heap usage: 1 allocs, 1 frees, 4 bytes allocated
==3453750==
==3453750== All heap blocks were freed -- no leaks are possible
==3453750==
==3453750== For lists of detected and suppressed errors, rerun with: -s
==3453750== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

#### ASan Report
```sh
$ gcc ./use-after-free.c -fsanitize=address -o use-after-free
$ ./use-after-free
```

```
=================================================================
==3454347==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000000010 at pc 0x556e884161d2 bp 0x7fff8fb90e50 sp 0x7fff8fb90e40
WRITE of size 4 at 0x602000000010 thread T0
    #0 0x556e884161d1 in main (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/use-after-free+0x11d1)
    #1 0x7f93b243c78f  (/usr/lib/libc.so.6+0x2378f)
    #2 0x7f93b243c849 in __libc_start_main (/usr/lib/libc.so.6+0x23849)
    #3 0x556e884160a4 in _start (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/use-after-free+0x10a4)

0x602000000010 is located 0 bytes inside of 4-byte region [0x602000000010,0x602000000014)
freed by thread T0 here:
    #0 0x7f93b26be672 in __interceptor_free /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:52
    #1 0x556e8841619a in main (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/use-after-free+0x119a)
    #2 0x7f93b243c78f  (/usr/lib/libc.so.6+0x2378f)

previously allocated by thread T0 here:
    #0 0x7f93b26bfa89 in __interceptor_malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x556e8841618a in main (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/use-after-free+0x118a)
    #2 0x7f93b243c78f  (/usr/lib/libc.so.6+0x2378f)

SUMMARY: AddressSanitizer: heap-use-after-free (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/use-after-free+0x11d1) in main
Shadow bytes around the buggy address:
  0x0c047fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c047fff8000: fa fa[fd]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==3454347==ABORTING
```

Both Valgrind and ASan detected the error.

### 5. Use-after-return
#### Malfunction Code
**[** use-after-return.c **]**:
```c
int *p;

void f(void) {
    int a = 4;
    p = &a;
}

int main(void) {
    f();
    *p = 1;
    return 0;
}
```

#### Valgrind Report
```sh
$ gcc ./use-after-return.c -o use-after-return
$ valgrind ./use-after-return
```

```
==52166== Memcheck, a memory error detector
==52166== Copyright (C) 2002-2022, and GNU GPL'd, by Julian Seward et al.
==52166== Using Valgrind-3.20.0 and LibVEX; rerun with -h for copyright info
==52166== Command: ./use-after-return
==52166==
==52166==
==52166== HEAP SUMMARY:
==52166==     in use at exit: 0 bytes in 0 blocks
==52166==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==52166==
==52166== All heap blocks were freed -- no leaks are possible
==52166==
==52166== For lists of detected and suppressed errors, rerun with: -s
==52166== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

#### ASan Report
```sh
$ gcc ./use-after-return.c -fsanitize=address -o use-after-return
$ ASAN_OPTIONS=detect_stack_use_after_return=1 ./use-after-return
```

```
=================================================================
==45351==ERROR: AddressSanitizer: stack-use-after-return on address 0x7efdb5000020 at pc 0x56127831f2ee bp 0x7ffcdb296900 sp 0x7ffcdb2968f0
WRITE of size 4 at 0x7efdb5000020 thread T0
    #0 0x56127831f2ed in main (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/use-after-return+0x12ed)
    #1 0x7efdb743c78f  (/usr/lib/libc.so.6+0x2378f)
    #2 0x7efdb743c849 in __libc_start_main (/usr/lib/libc.so.6+0x23849)
    #3 0x56127831f0c4 in _start (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/use-after-return+0x10c4)

Address 0x7efdb5000020 is located in stack of thread T0 at offset 32 in frame
    #0 0x56127831f1a8 in f (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/use-after-return+0x11a8)

  This frame has 1 object(s):
    [32, 36) 'a' (line 4) <== Memory access at offset 32 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return (/home/alan/Assignment/Senior/Second_Semester/Software_Testing/0816066-ST-2023/Lab06/use-after-return+0x12ed) in main
Shadow bytes around the buggy address:
  0x0fe0369f7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0369f7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0369f7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0369f7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0369f7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0fe0369f8000: f5 f5 f5 f5[f5]f5 f5 f5 00 00 00 00 00 00 00 00
  0x0fe0369f8010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0369f8020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0369f8030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0369f8040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0369f8050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==45351==ABORTING
```

Only ASan detected the error.
However, ASan required an option be enabled to detect the error.

## Experiment 2

### Malfunction Code
**[** stack-oob-across-red-zone.c **]**:
```c
int main(void) {
    int a[8];
    int b[8];
    a[16] = 1;
    return 0;
}
```

ASan failed to detect the error.
It could detect the stack-out-of-bound error however, if we assigned the value to `a` with index between 8 and 15.
