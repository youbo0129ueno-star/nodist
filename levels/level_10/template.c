#include <stdio.h>
#include <stddef.h>

/* TODO: struct DNode を定義する */

int main(void) {
    int x;
    scanf("%d", &x);

    struct DNode node;
    node.prev = NULL;
    node.key = x;
    node.next = NULL;

    printf(
        "%d %s %s\n",
        node.key,
        node.prev == NULL ? "NULL" : "NOT NULL",
        node.next == NULL ? "NULL" : "NOT NULL"
    );
    return 0;
}
