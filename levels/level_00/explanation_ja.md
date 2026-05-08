## 方針

このレベルでは、リストの最小単位である「ノード」を構造体で表します。

## ポイント

リストは値だけでなく、「次に進むための情報」を各セルが持ちます。Cではその情報をポインタで表します。

```c
struct Node {
    int key;
    struct Node *next;
};
```

`next` は次の `struct Node` を指すポインタです。まだ次のノードがないときは `NULL` を入れます。

## 典型手順

1. `struct Node` を定義します。
2. `struct Node node;` で1個のノードを作ります。
3. `node.key` に入力値を入れます。
4. `node.next` に `NULL` を入れます。
5. `node.next == NULL` を確認して出力します。

## 注意点

構造体の中で `Node *next;` とだけ書くと、この時点では `Node` という型名はまだ定義されていません。`typedef` を使わない場合は `struct Node *next;` と書きます。
