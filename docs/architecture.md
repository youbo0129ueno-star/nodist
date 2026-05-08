# Architecture

このリポジトリは Pandit 形式を参考にした、ローカルCLI型のC言語アルゴリズム演習です。

## Layers

1. CLI layer: `app/cli.py`
2. Level asset layer: `app/registry.py`
3. C judge layer: `app/judge.py`
4. Progress layer: `app/progress.py`

## Runtime Flow

### `nodist list`

- `levels/*/meta.json` を読み込む
- `~/.nodist/progress.json` の進捗と照合する
- `COMPLETED`, `UNLOCKED`, `LOCKED` を表示する

### `nodist level <id>`

- レベルの解放状態を確認する
- `task_ja.md` または `task.md` を表示する
- カレントディレクトリの `answer.c` を `template.c` で上書きする

### `nodist submit <id> [answer.c]`

1. レベルの解放状態を確認する
2. 提出Cファイルを一時ディレクトリでコンパイルする
3. `tests.json` の各ケースを標準入力として実行する
4. 標準出力と `expected` を完全一致で比較する
5. すべて通れば進捗を更新する

### `nodist __validate_levels`

- レベル資産の必須ファイルを確認する
- `meta.json` の必須フィールドと `previous_level` を確認する
- `tests.json` の形式を確認する
- 各レベルの `answer.c` が全テストを通ることを確認する
- 教材作成者向けの裏コマンドとして扱う

## Level Asset Layout

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

## Compatibility

`python3 src/judge.py <level_id> <file.c>` は直接採点用として残しています。
