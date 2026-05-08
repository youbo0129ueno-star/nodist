#include <stdio.h>
#include <stdlib.h>

struct DNode {
    struct DNode *prev;
    int key;
    struct DNode *next;
};

struct DNode *create_node(int key) {
    struct DNode *node = malloc(sizeof(struct DNode));
    if (node == NULL) {
        exit(1);
    }
    node->prev = NULL;
    node->key = key;
    node->next = NULL;
    return node;
}

struct DNode *append_tail(struct DNode *head, int key) {
    struct DNode *node = create_node(key);
    if (head == NULL) {
        return node;
    }
    struct DNode *current = head;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = node;
    node->prev = current;
    return head;
}

struct DNode *node_at(struct DNode *head, int pos) {
    struct DNode *current = head;
    for (int i = 0; current != NULL && i < pos; i++) {
        current = current->next;
    }
    return current;
}

struct DNode *insert_after(struct DNode *head, struct DNode *p, int key) {
    struct DNode *x = create_node(key);
    /* TODO: p の次に x を挿入し、新しい head を返す */
}

void print_list(struct DNode *head) {
    for (struct DNode *current = head; current != NULL; current = current->next) {
        printf("%d", current->key);
        if (current->next != NULL) {
            printf(" ");
        }
    }
    printf("\n");
}

void free_list(struct DNode *head) {
    while (head != NULL) {
        struct DNode *next = head->next;
        free(head);
        head = next;
    }
}

int main(void) {
    int n, pos, value;
    scanf("%d %d %d", &n, &pos, &value);

    struct DNode *head = NULL;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        head = append_tail(head, x);
    }

    struct DNode *p = pos == -1 ? NULL : node_at(head, pos);
    head = insert_after(head, p, value);
    print_list(head);
    free_list(head);
    return 0;
}
