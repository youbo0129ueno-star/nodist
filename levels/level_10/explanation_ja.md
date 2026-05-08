## 方針

このレベルでは、単方向リストの `next` に加えて、前のノードを指す `prev` を持つ構造体を定義します。

## ポイント

双方向リストのノードは、前後どちらにも進めるようにします。

```c
struct DNode {
    struct DNode *prev;
    int key;
    struct DNode *next;
};
```

1個だけのノードは前にも後ろにも何もないので、`prev` も `next` も `NULL` です。

## 注意点

`prev` と `next` はどちらも同じ型のノードを指します。構造体の中では `struct DNode *prev;` のように `struct` 付きで書きます。
