#include <stdlib.h>

int main(void) {
    int* a = (int*) malloc(4 * sizeof(int));
    a[5] = 1;
    free(a);
    return 0;
}
