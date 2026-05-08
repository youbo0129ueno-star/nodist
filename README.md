# algo-trainer

アルゴリズムとデータ構造の講義内容と、実際にC言語でコードを書く演習の難易度差を埋めるためのCLI教材リポジトリです。

## 目的

- 学生が `git clone` してすぐ使える教材にする
- C言語のアルゴリズム演習をローカルの `gcc` または `clang` で自動採点する
- 将来的にGitHub PagesでWeb GUI化できるよう、問題データと採点ロジックを分離する

## セットアップ方法

### 前提条件

- Python 3.9以上
- `gcc` または `clang`
- macOS または Linux

### インストール

```bash
git clone <this-repository-url>
cd algo-trainer
python3 --version
gcc --version
```

Pythonの外部パッケージは使っていません。`requirements.txt` は将来の依存追加用に置いています。

## 実行例

```bash
python3 src/judge.py linear_search submissions/linear_search.c
```

出力例:

```text
=== linear_search ===
Compiler: clang
Compile: OK
Test sample1: AC (0.000s)
Test not_found: AC (0.000s)
Test first_position: AC (0.000s)

Result: 3/3 passed
```

まとめて動かす場合:

```bash
make test
```

## 問題一覧

- `linear_search`: 配列 `A` から値 `x` を探し、見つかれば0-indexedの位置、なければ `-1` を出力
- `max_value`: 配列 `A` の最大値を出力
- `binary_search`: 昇順配列 `A` から値 `x` を二分探索し、見つかれば0-indexedの位置、なければ `-1` を出力

## 採点器の仕様

```bash
python3 src/judge.py <problem_id> <submission_file>
```

採点器は次の流れで動きます。

1. `problems/<problem_id>/tests.json` を読む
2. 指定された提出Cファイルを一時ディレクトリでコンパイルする
3. 各テストケースの入力を標準入力に渡して実行する
4. 標準出力が期待値と完全一致するか判定する
5. 最後に `Result: 2/3 passed` のように集計を表示する

コンパイルには以下のオプションを使います。

```text
-std=c11 -Wall -Wextra
```

結果の種類:

| 表示 | 意味 |
| --- | --- |
| AC | 正解。出力が期待値と完全一致した |
| WA | 不正解。出力が期待値と一致しない |
| CE | コンパイルエラー |
| RE | 実行時エラー |
| TLE | 実行時間制限超過 |

実行時間制限はMVPでは2秒です。`src/judge.py` の `TIME_LIMIT_SECONDS` で管理しています。

## tests.json の形式

```json
[
  {
    "name": "sample1",
    "input": "5 3\n1 2 3 4 5\n",
    "expected": "2\n"
  },
  {
    "name": "not_found",
    "input": "5 9\n1 2 3 4 5\n",
    "expected": "-1\n"
  }
]
```

- `name`: テストケース名
- `input`: 標準入力に渡す文字列
- `expected`: 期待する標準出力

## 問題の追加方法

1. `problems/<problem_id>/` を作る
2. `statement.md`, `template.c`, `solution.c`, `tests.json` を追加する
3. 正解例が通ることを確認する

```bash
python3 src/judge.py <problem_id> problems/<problem_id>/solution.c
```

学生用の提出ファイルを用意する場合は、`problems/<problem_id>/template.c` を `submissions/<problem_id>.c` にコピーして使います。

## ディレクトリ構成

```text
algo-trainer/
├── README.md
├── Makefile
├── requirements.txt
├── src/
│   └── judge.py
├── problems/
│   ├── linear_search/
│   ├── max_value/
│   └── binary_search/
├── submissions/
└── docs/
    └── roadmap.md
```

## セキュリティ上の注意

この採点器はローカル教材用のMVPです。提出されたCコードを実際にコンパイルして実行するため、危険なコード実行を完全には防げません。

不信頼なコードをサーバー上で実行する用途には使わないでください。将来的にオンライン化する場合は、コンテナ分離、権限制限、ファイルシステム制限、ネットワーク制限などを別途設計する必要があります。

## 将来的なWeb GUI化構想

問題文はMarkdown、テストケースはJSONとして管理しているため、GitHub Pages上のWeb GUIから同じ問題データを読み込めます。まずはブラウザで問題文とテンプレートを表示し、ローカルCLIで採点する形を維持します。その後、採点結果JSON出力やブラウザ内エディタを追加すると、CLIとWebの両方で同じ教材データを使えるようになります。

今後の開発タスクは [docs/roadmap.md](docs/roadmap.md) にまとめています。
