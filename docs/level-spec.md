# Level Spec

各レベルは `levels/level_XX/` に置きます。

## Required Files

- `meta.json`
- `task_ja.md` または `task.md`
- `template.c`
- `answer.c`
- `tests.json`

Recommended:

- `explanation_ja.md`
- `explanation.md`

## `meta.json`

```json
{
  "id": "level_00",
  "title": "Linear Search",
  "title_ja": "線形探索",
  "previous_level": null,
  "hints": ["Check each element."],
  "hints_ja": ["各要素を順番に確認します。"]
}
```

Minimum fields:

- `id`
- `title`
- `previous_level`
- `hints`

Japanese fields are optional but recommended:

- `title_ja`
- `hints_ja`

## `tests.json`

```json
[
  {
    "name": "sample1",
    "input": "5 3\n1 2 3 4 5\n",
    "expected": "2\n"
  }
]
```

## C Program Contract

提出コードは標準入力から読み、標準出力に答えだけを出力します。

採点器は次のオプションでコンパイルします。

```text
-std=c11 -Wall -Wextra
```

## Authoring Guidelines

- 1レベルに主な学習目標を1つだけ置く
- 入力形式と出力形式を明確に書く
- 最初のテストは問題文のサンプルと対応させる
- 境界値を少なくとも1つ入れる
- ヒントは答えそのものではなく、考え方を段階的に示す
