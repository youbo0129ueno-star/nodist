#include <stdio.h>
#include <stdlib.h>

struct Node {
    int key;
    struct Node *next;
};

int main(void) {
    int x;
    scanf("%d", &x);

    /* TODO: malloc で struct Node を1個確保する */

    if (node == NULL) {
        return 1;
    }

    node->key = x;
    node->next = NULL;

    printf("%d %s\n", node->key, node->next == NULL ? "NULL" : "NOT NULL");

    /* TODO: node を解放する */
    return 0;
}
