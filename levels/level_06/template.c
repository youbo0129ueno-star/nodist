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

int list_contains(struct Node *head, int target) {
    /* TODO: target が見つかれば 1、なければ 0 を返す */
}

void free_list(struct Node *head) {
    while (head != NULL) {
        struct Node *next = head->next;
        free(head);
        head = next;
    }
}

int main(void) {
    int n, target;
    scanf("%d %d", &n, &target);
    struct Node *head = NULL;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        head = append_tail(head, x);
    }
    printf("%s\n", list_contains(head, target) ? "FOUND" : "NOT FOUND");
    free_list(head);
    return 0;
}
