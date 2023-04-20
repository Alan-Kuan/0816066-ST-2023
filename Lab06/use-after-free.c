#include <stdlib.h>

int main(void) {
    int* a = (int*) malloc(sizeof(int));
    free(a);
    *a = 1;
    return 0;
}
