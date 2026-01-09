# Prompting

## Dummy files
- dummy1: 
- dummy2: https://github.com/MiroMindAI/MiroThinker/blob/main/libs/miroflow-tools/src/miroflow_tools/mcp_servers/searching_google_mcp_server.py
- dummy3: https://github.com/numpy/numpy/blob/maintenance/1.26.x/numpy/distutils/system_info.py
- dummy4.py: https://github.com/numpy/numpy/blob/maintenance/1.26.x/numpy/distutils/misc_util.py

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
- How to Write Docstrings in Python: https://realpython.com/how-to-write-docstrings-in-python/#docstrings-for-functions 

## Length of the input of the API call
- What's your average .py file length?:
https://www.reddit.com/r/learnpython/comments/198j2r2/whats_your_average_py_file_lenght/
(until 500 without docstrings; 1000 is long; 2000 limit)
- Gemini official website: https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash
  
  For Gemini models, a token is equivalent to about 4 characters. 100 tokens is equal to about 60-80 English words.

  Gemini 2.5 Flash model: 
  - input token limit 1,000,000 ~ 4,000,000 characters ~ 50,000 lines [1]
  - output token limit 65,536

- [1] PEP 8 – Style Guide for Python Code: https://peps.python.org/pep-0008/#:~:text=spaces%20for%20indentation.-,Maximum%20Line%20Length,be%20limited%20to%2072%20characters.

  Limit all lines to a maximum of 79 characters.

## Prompt engineering (prompt templates)
- task, context, exemplar, persona, format, (tone)

### References
- "Prompt design strategies": https://ai.google.dev/gemini-api/docs/prompting-strategies

### Results

dummy3
_parse_env_order

#### プロンプトを日本語で：

```
"""環境変数から順序設定を解析し、基本リストに基づいて許可される項目と未知の項目を返す。

引数:
    base_order (list of str): 比較の基準となる基本順序の項目リスト
    env (str): 順序文字列を取得する環境変数の名前

戻り値:
    tuple: (list of str, list of str) - (許可される順序の項目リスト, 基本順序に存在しない未知の項目リスト)

送出する例外:
    ValueError: 環境変数文字列のフォーマットが無効な場合
"""
```

#### プロンプトを英語で：

```
"""環境変数から順序文字列を解析し、許可された順序と不明な順序のリストを返す。

引数:
    base_order (list of str): 基本となる順序のリスト
    env (str): 読み取る環境変数の名前

戻り値:
    tuple (list of str, list of str):
        許可された順序の要素のリストと、base_orderに含まれない不明な順序の要素のリスト       

送出する例外:
    ValueError: 環境変数で指定された順序文字列に、複数の否定プレフィックスが含まれている場合 、または否定プレフィックスと非否定アイテムが混在している場合

制約:
    環境変数 `env` が存在しない場合、`base_order` がそのまま返され、不明な順序のリストは空と なる
"""
```

#### オリジナル版

```
""" Parse an environment variable `env` by splitting with "," and only returning elements from `base_order`

    This method will sequence the environment variable and check for their
    individual elements in `base_order`.

    The items in the environment variable may be negated via '^item' or '!itema,itemb'.
    It must start with ^/! to negate all options.

    Raises
    ------
    ValueError: for mixed negated and non-negated orders or multiple negated orders

    Parameters
    ----------
    base_order : list of str
       the base list of orders
    env : str
       the environment variable to be parsed, if none is found, `base_order` is returned

    Returns
    -------
    allow_order : list of str
        allowed orders in lower-case
    unknown_order : list of str
        for values not overlapping with `base_order`
    """
```

## Comment types
- Program general explanation
- Function level ( ← now )
- Code line level (ex.: unfamiliar modules)