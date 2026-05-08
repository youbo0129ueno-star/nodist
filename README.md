# nodist

アルゴリズムとデータ構造の講義内容と、実際にC言語でコードを書く演習の難易度差を埋めるためのCLI教材です。

構成と体験は Pandit 形式を参考にしています。`levels/level_XX/` に問題データを置き、CLIから `list`, `level`, `hint`, `answer`, `explain`, `submit` を使って段階的に進めます。

## 目的

- 学生が `git clone` してすぐ使える教材にする
- C言語のアルゴリズム演習をローカルの `gcc` または `clang` で自動採点する
- 将来的にGitHub PagesでWeb GUI化できるよう、レベル資産と採点ロジックを分離する

## セットアップ

前提:

- Python 3.9以上
- `gcc` または `clang`
- macOS または Linux

そのまま使う場合:

```bash
git clone <this-repository-url>
cd nodist
python3 -m app.cli list
```

Pandit の `pandit list` と同じように、この教材では `nodist` コマンドを使います。

```bash
python3 -m pip install -e .
nodist list
```

以後は `python3 -m app.cli ...` ではなく、次のように起動できます。

```bash
nodist list
nodist level level_00
nodist submit level_00
```

Pythonの外部パッケージは使っていません。

## 主なコマンド

```bash
nodist list
nodist level level_00
nodist hint level_00
nodist answer level_00
nodist explain level_00
nodist submit level_00
```

`level` コマンドは、カレントディレクトリの `answer.c` をそのレベルのテンプレートで上書きします。作業ファイルは常に1つだけです。

## 実行例

```bash
nodist level level_00
nodist submit level_00
```

直接採点だけしたい場合:

```bash
python3 src/judge.py level_00 levels/level_00/answer.c
```

まとめて正解例を確認する場合:

```bash
make test
```

教材作成者向けの裏検証コマンド:

```bash
nodist __validate_levels
make validate
```

## レベル一覧

- `level_00`: `struct Node` を定義する
- `level_01`: `malloc` で1個のノードを作る
- `level_02`: 2個のノードを `next` でつなぐ
- `level_03`: 先頭から末尾まで走査する
- `level_04`: 末尾にノードを追加する
- `level_05`: 先頭にノードを追加する
- `level_06`: リストから値を探す
- `level_07`: 見つかったノードへのポインタを返す
- `level_08`: 指定値のノードを削除する
- `level_09`: リスト全体を解放する
- `level_10`: 双方向リストの `Node` を定義する
- `level_11`: 双方向リストへ途中挿入する
- `level_12`: 双方向リストからノードを削除する
- `level_13`: 最大値・最小値を求める
- `level_14`: リスト操作の計算量を答える

進捗は `~/.nodist/progress.json` に保存されます。最初は `level_00` だけが解放され、クリアすると次のレベルが解放されます。

## レベル構成

```text
levels/
  level_00/
    meta.json
    task_ja.md
    task.md
    explanation_ja.md
    template.c
    answer.c
    tests.json
```

`meta.json` はタイトル、前提レベル、ヒントを管理します。`task_ja.md` と `task.md` は問題文です。`tests.json` は採点用テストケースです。

詳しい仕様は [docs/level-spec.md](docs/level-spec.md) を参照してください。

教材全体の分割案は [docs/curriculum.md](docs/curriculum.md) にまとめています。

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

採点では標準出力が `expected` と完全一致する必要があります。

## 採点器の仕様

提出Cファイルは一時ディレクトリでコンパイルされます。

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

実行時間制限はMVPでは2秒です。

`submit` はデフォルトでカレントディレクトリの `answer.c` を提出します。別ファイルを採点したい場合だけ、明示的に指定できます。

```bash
nodist submit level_00 path/to/file.c
```

## 新しいレベルの追加方法

1. `levels/level_XX/` を作る
2. `meta.json`, `task_ja.md`, `template.c`, `answer.c`, `tests.json` を追加する
3. 正解例が通ることを確認する

```bash
python3 src/judge.py level_XX levels/level_XX/answer.c
```

## ディレクトリ構成

```text
nodist/
├── app/
│   ├── cli.py
│   ├── config.py
│   ├── judge.py
│   ├── progress.py
│   └── registry.py
├── docs/
│   ├── architecture.md
│   ├── level-spec.md
│   └── roadmap.md
├── levels/
│   ├── level_00/
│   ├── level_01/
│   └── level_14/
├── src/
│   └── judge.py
├── Makefile
├── pyproject.toml
└── README.md
```

## セキュリティ上の注意

この採点器はローカル教材用のMVPです。提出されたCコードを実際にコンパイルして実行するため、危険なコード実行を完全には防げません。

不信頼なコードをサーバー上で実行する用途には使わないでください。将来的にオンライン化する場合は、コンテナ分離、権限制限、ファイルシステム制限、ネットワーク制限などを別途設計する必要があります。

## 将来的なWeb GUI化構想

問題文はMarkdown、テストケースはJSON、メタ情報は `meta.json` として管理しているため、GitHub Pages上のWeb GUIから同じレベル資産を読み込めます。まずはCLIで進捗と採点を完成させ、その後に採点結果JSON出力やブラウザ内エディタを追加すると、CLIとWebの両方で同じ教材データを使えるようになります。
