## 方針

このレベルでは、リスト操作の基本である「先頭から順にたどる」処理を書きます。

## ポイント

配列なら添字 `i` を増やしますが、リストではポインタを次のノードへ進めます。

```c
struct Node *current = head;
while (current != NULL) {
    ...
    current = current->next;
}
```

`current == NULL` になったら、もうノードは存在しません。

## 典型手順

1. `current` を `head` で初期化します。
2. `current != NULL` の間ループします。
3. `current->key` を出力します。
4. `current = current->next` で次へ進みます。

## 注意点

`current = current->next` を忘れると、同じノードを見続ける無限ループになります。
