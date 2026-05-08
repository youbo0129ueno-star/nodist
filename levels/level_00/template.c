#include <stdio.h>
#include <stddef.h>

/* TODO: struct Node を定義する */

int main(void) {
    int x;
    scanf("%d", &x);

    struct Node node;
    node.key = x;
    node.next = NULL;

    printf("%d %s\n", node.key, node.next == NULL ? "NULL" : "NOT NULL");
    return 0;
}
