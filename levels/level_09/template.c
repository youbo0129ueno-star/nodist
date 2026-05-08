#include <stdio.h>
#include <stdlib.h>

struct Node {
    int key;
    struct Node *next;
};

struct Node *create_node(int key) {
    struct Node *node = malloc(sizeof(struct Node));
    if (node == NULL) {
        exit(1);
    }
    node->key = key;
    node->next = NULL;
    return node;
}

struct Node *append_tail(struct Node *head, int key) {
    struct Node *node = create_node(key);
    if (head == NULL) {
        return node;
    }
    struct Node *current = head;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = node;
    return head;
}

int free_list(struct Node *head) {
    /* TODO: 全ノードを解放し、解放した個数を返す */
}

int main(void) {
    int n;
    scanf("%d", &n);
    struct Node *head = NULL;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        head = append_tail(head, x);
    }
    printf("freed %d\n", free_list(head));
    return 0;
}
