#include <stdio.h>
#include <string.h>

const char *complexity_of(const char *operation) {
    /* TODO: operation に対応する計算量文字列を返す */
}

int main(void) {
    char operation[64];
    scanf("%63s", operation);
    printf("%s\n", complexity_of(operation));
    return 0;
}
