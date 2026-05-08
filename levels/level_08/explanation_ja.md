## 方針

単方向リストでは、削除対象の1つ前のノードが必要です。そのため `prev` と `current` の2つを持って進みます。

## ポイント

途中のノードを削除する場合は、

```c
prev->next = current->next;
free(current);
```

で前のノードから次のノードへ直接つなぎます。

先頭を削除する場合は `prev` が存在しないため、

```c
head = current->next;
```

として `head` を更新します。

## 注意点

`free(current)` した後に `current->next` を読むのは危険です。必要なポインタは `free` より前に使うか、先に変数へ保存します。
