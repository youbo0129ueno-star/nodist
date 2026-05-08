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

struct Node *list_minimum(struct Node *head) {
    /* TODO: 最小値を持つノードへのポインタを返す */
}

struct Node *list_maximum(struct Node *head) {
    /* TODO: 最大値を持つノードへのポインタを返す */
}

void free_list(struct Node *head) {
    while (head != NULL) {
        struct Node *next = head->next;
        free(head);
        head = next;
    }
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

    struct Node *min_node = list_minimum(head);
    struct Node *max_node = list_maximum(head);
    printf("%d %d\n", min_node->key, max_node->key);

    free_list(head);
    return 0;
}
