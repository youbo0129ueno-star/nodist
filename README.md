# algo-trainer

アルゴリズムとデータ構造の講義内容と、実際にC言語でコードを書く演習の難易度差を埋めるためのCLI教材リポジトリです。

## 目的

- 学生が `git clone` してすぐ使える教材を提供
- C言語のアルゴリズム演習をローカルの gcc/clang で自動採点
- 将来的に GitHub Pages による Web GUI化に対応できるよう、問題データと採点ロジックを分離

## セットアップ方法

### 前提条件

- Python 3.8 以上
- gcc または clang (macOS / Linux)
- git

### インストール

```bash
git clone https://github.com/youbo0129ueno-star/algo-trainer.git
cd algo-trainer
pip install -r requirements.txt
```

## 使い方

### 採点の実行

```bash
python3 src/judge.py <problem_id> <submission_file>
```

**例：**

```bash
# linear_search 問題を採点
python3 src/judge.py linear_search submissions/linear_search.c

# max_value 問題を採点
python3 src/judge.py max_value submissions/max_value.c

# binary_search 問題を採点
python3 src/judge.py binary_search submissions/binary_search.c
```

### 実行例

```
$ python3 src/judge.py linear_search submissions/linear_search.c
=== linear_search ===

Compile: OK
Memory: 3.2 MB

Test sample1: AC (0.001s)
Test not_found: AC (0.001s)
Test edge_case: WA (0.001s)

Result: 2/3 passed ❌
```

## 問題構成

各問題は以下の構成を持ちます：

```
problems/<problem_id>/
├── statement.md      # 問題文
├── template.c        # 学生用テンプレート
├── solution.c        # 正解例
└── tests.json        # テストケース定義
```

### テストケースの形式 (tests.json)

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

**フィールド説明:**

- `name`: テストケースの名前（ログに表示）
- `input`: 標準入力として与えるデータ
- `expected`: 期待される標準出力

## 問題一覧

### 1. linear_search（線形探索）

配列 A から値 x を線形探索し、見つかれば 0-indexed の位置、なければ -1 を出力します。

**入力形式:**
```
n x
a[0] a[1] ... a[n-1]
```

**出力形式:**
```
位置 (0-indexed) または -1
```

### 2. max_value（最大値探索）

配列 A の最大値を出力します。

**入力形式:**
```
n
a[0] a[1] ... a[n-1]
```

**出力形式:**
```
最大値
```

### 3. binary_search（二分探索）

昇順配列 A から値 x を二分探索で見つけ、見つかれば 0-indexed の位置、なければ -1 を出力します。

**入力形式:**
```
n x
a[0] a[1] ... a[n-1]
```

**出力形式:**
```
位置 (0-indexed) または -1
```

## 採点器の仕様

### コンパイルオプション

```
-std=c11 -Wall -Wextra
```

### 採点結果の種類

| 結果 | 意味 |
|------|------|
| AC (Accepted) | 正解。出力が完全に一致した |
| WA (Wrong Answer) | 不正解。出力が期待値と異なる |
| CE (Compilation Error) | コンパイルエラーが発生した |
| RE (Runtime Error) | 実行時エラーが発生した（セグメンテーション違反など） |
| TLE (Time Limit Exceeded) | 実行時間が制限を超えた |

### 実行時間制限

デフォルト: **2秒**

## 新しい問題の追加方法

1. **問題ディレクトリを作成**

```bash
mkdir -p problems/your_problem_id
```

2. **4つのファイルを作成**

- `statement.md`: 問題文
- `template.c`: 学生用テンプレート
- `solution.c`: 正解例
- `tests.json`: テストケース

3. **テストで動作確認**

```bash
python3 src/judge.py your_problem_id problems/your_problem_id/solution.c
```

## 技術構成

- **言語**: Python 3, C11
- **テストケース管理**: JSON
- **問題文管理**: Markdown
- **コンパイラ**: gcc または clang

## セキュリティに関する注意

このツールはローカル環境を想定した教育用ツールです。不信頼できるコードの実行を完全には防げません。

- 必ずローカル環境でのみ使用してください
- サーバー環境での使用は推奨されません
- 悪意あるコードが実行される可能性を完全には排除できません

## 将来の展開予定

- **Web GUI**: GitHub Pages を使った Web ブラウザでの提出機能
- **オンラインジャッジ化**: サーバー化による複数ユーザー対応
- **リアルタイム採点**: 提出時の自動採点通知
- **ランキング機能**: 解いた問題数や実行時間でランク表示
- **ディスカッション機能**: 問題ごとのディスカッション

詳しくは [roadmap.md](docs/roadmap.md) をご覧ください。

## ライセンス

MIT

## 作成者

youbo0129ueno-star
