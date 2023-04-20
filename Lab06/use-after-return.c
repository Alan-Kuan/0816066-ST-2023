int* f(void) {
    int a = 4;
    return &a;
}

int main(void) {
    int* a = f();
    *a = 1;
    return 0;
}
