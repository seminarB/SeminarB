# Prompting

## API call
get the API key:
https://aistudio.google.com/app/api-keys

how to API call:
https://ai.google.dev/gemini-api/docs/quickstart

API libraries installation (pip-25.3):
pip install -U google-genai python-dotenv
python.exe -m pip install --upgrade pip

GitHub Secrets:
1. Go to GitHub Website (for the repository running the Action)
2. "Settings" → "Secrets and variables" → "Actions"
3. "New repository secret"
4. Name: GEMINI_API_KEY
5. Paste API key

## Python best practice for comment writing
- docstring (more than one line) right beneath the declaration of the function
- D.R.Y.: don't repeat yourself
- do not be rude
- Docstring Conventions (check References)
  - 3 double-quotes + summary on the same line
  - summary line: imperative verb; summarize the function's behavior
  - blank line
  - "Keyword arguments:"
  - document its arguments, return value(s), side effects, exceptions raised, and restrictions on when it can be called (all if applicable). Optional arguments should be indicated. It should be documented whether keyword arguments are part of the interface.
  - 3 double-quotes

### References
- "PEP 257 – Docstring Conventions": https://peps.python.org/pep-0257/
- Stack Overflow thread: https://stackoverflow.com/questions/2357230/what-is-the-proper-way-to-comment-functions-in-python 


## Prompt engineering (prompt templates)
- task, context, exemplar, persona, format, (tone)

### References
- "Prompt design strategies": https://ai.google.dev/gemini-api/docs/prompting-strategies

### Results

```
def fun(x):
    if (x % 3 == 0):
        print("multiple of 3")
    else:
        print("not multiple of 3")
```

#### プロンプトを日本語で：

```
"""入力された整数が3の倍数であるかを判定し、結果を標準出力に出力する。

引数:
x -- 3の倍数であるかを判定する対象の整数。

副作用:
標準出力に判定結果の文字列（"multiple of 3" または "not multiple of 3"）を出力します。

制約事項:
xは整数である必要があります。"""
```

#### プロンプトを英語で：

```
"""与えられた数値が3の倍数であるかを判定し、その結果を出力します。

引数:
x -- 判定する数値。

副作用:
xが3の倍数である場合 "multiple of 3" を、そうでない場合 "not multiple of 3" を標準出力に出力 します。

制約:
xは整数または整数との剰余演算(%)が可能な型である必要があります。それ以外の型の場合、TypeErrorが発生する可能性があります。"""
```

## Comment types
- Program general explanation
- Function level ( ← now )
- Code line level (ex.: unfamiliar modules)