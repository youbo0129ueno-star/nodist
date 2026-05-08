#include <stdio.h>
#include <stdlib.h>

struct Node {
    int key;
    struct Node *next;
};

int main(void) {
    int a, b;
    scanf("%d %d", &a, &b);

    struct Node *first = malloc(sizeof(struct Node));
    struct Node *second = malloc(sizeof(struct Node));
    if (first == NULL || second == NULL) {
        free(first);
        free(second);
        return 1;
    }

    first->key = a;
    second->key = b;

    /* TODO: first と second を next でつなぐ */

    printf("%d %d\n", first->key, first->next->key);

    free(second);
    free(first);
    return 0;
}
