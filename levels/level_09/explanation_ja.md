## 方針

このレベルでは、動的に確保したリストを最後まで安全に解放します。

## ポイント

現在のノードを `free` すると、そのノードのメンバはもう読めません。そのため、先に次のノードを保存します。

```c
struct Node *next = current->next;
free(current);
current = next;
```

## 典型手順

1. `current` を `head` にします。
2. `current != NULL` の間ループします。
3. `next = current->next` を保存します。
4. `free(current)` します。
5. `current = next` で次へ進みます。
6. 解放数を返します。

## 注意点

`free(current); current = current->next;` は危険です。`free` 済みのメモリを読もうとしているためです。
