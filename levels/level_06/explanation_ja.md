## 方針

このレベルでは、講義ノートの `List-Search` を構造体ポインタ版で書きます。

## ポイント

探索は `head` から始め、`next` を順にたどります。現在地の値が目標値と一致すれば成功です。

```c
while (current != NULL) {
    if (current->key == target) {
        return 1;
    }
    current = current->next;
}
return 0;
```

## 注意点

見つかった後も最後まで走査する必要はありません。見つかった時点で `return 1` すると、余計な処理をせずに終われます。
