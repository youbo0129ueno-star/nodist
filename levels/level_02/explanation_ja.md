## 方針

このレベルでは、ポインタによって「次のノード」を表します。

## ポイント

2個のノード `first` と `second` があるとき、

```c
first->next = second;
second->next = NULL;
```

とすると、`first` から `second` へ進めるリストになります。

## 典型手順

1. 2個のノードを `malloc` で作ります。
2. それぞれの `key` に入力値を入れます。
3. `first->next = second` にします。
4. `second->next = NULL` にします。
5. `first` から `next` をたどって出力します。

## 注意点

`first` と `second` がメモリ上で隣にある必要はありません。リストの順番は、物理的な配置ではなく `next` の向きで決まります。
