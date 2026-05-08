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

struct Node *push_front(struct Node *head, int key) {
    struct Node *node = create_node(key);
    /* TODO: node を先頭につなぎ、新しい head を返す */
}

void print_list(struct Node *head) {
    for (struct Node *current = head; current != NULL; current = current->next) {
        printf("%d", current->key);
        if (current->next != NULL) {
            printf(" ");
        }
    }
    printf("\n");
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
    int x;
    scanf("%d", &x);
    head = push_front(head, x);
    print_list(head);
    free_list(head);
    return 0;
}
