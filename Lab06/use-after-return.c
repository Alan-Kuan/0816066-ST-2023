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
