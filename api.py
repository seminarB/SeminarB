import sys
import os
from google import genai
from dotenv import load_dotenv # API key (environment variable) is in .env file

# read .env file and load variables into the system
load_dotenv()

# check if API key was found
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: API key not found.")
    sys.exit(1) # error code

# the client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=api_key)

# catch the file (file to be commented) name from the command line
# command format: python api.py <filename> <function>

# TODO: for now, comments only first argument and ignores the rest
# check if there is an argument
if len(sys.argv) < 3:
    print("Usage: python api.py <filename> <function>")
    sys.exit(1)

# catch file name
filename = sys.argv[1]
function = sys.argv[2]

# try to open file and catch its content
try:
    with open(filename, "r", encoding="utf-8") as f:
        code_content = f.read()
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    sys.exit(1)

# API call prompt
# 日本語
prompt_jp = f'''
あなたは、以下のPythonコードを作成した経験豊富なプログラマです。
他の開発者がコードの動作を理解できるように、特定の関数にコメント（docstring）を追加しようとしています。

指定されたコードの中から「{function}」という名前の関数を見つけ、その機能の要約、引数、戻り値、副作用、送出される例外、および制約事項を記載した複数行のdocstringを作成してください。

1.docstringは3つの二重引用符で開始し、同じ行に関数の要約を記述してください。
2.その直後に空行を1つ入れてください。
3.続けて、引数、戻り値、副作用、送出される例外、制約事項、がそれぞれ存在する場合のみリストアップしてください。
4.該当しない項目は記述せず、省略してください。
5.最後に3つの二重引用符で閉じてください。
6.指定された関数がコード内に存在しない場合は、空文字のみを返してください。
7.コメントを日本語で書いてください。
8.出力には```python などのMarkdown記法は絶対に含まないでください。

例：
"""複素数を作成する。

引数:
real -- 実部 (default 0.0)
imag -- 虚部 (default 0.0)

制約事項:
数値は整数でなければならない"""

対象コード：
{code_content}

対象関数：
{function}
'''

# english
prompt_eng = f'''
You are an experienced programmer who created the Python code below.
You are trying to add comments (docstrings) to a specific function so that other developers can understand the code's behavior.

Find the function named "{function}" within the specified code, and create a multi-line docstring describing its function summary, arguments, return values, side effects, exceptions raised, and restrictions.

1. Start the docstring with three double quotes and write the function summary on the same line.
2. Insert one empty line immediately after that.
3. Then, list arguments, return values, side effects, exceptions raised, and restrictions only if they exist respectively.
4. Do not describe items that are not applicable; omit them.
5. Close with three double quotes at the end.
6. If the specified function does not exist in the code, return only an empty string.
7. Write the comment in Japanese.
8. Absolutely do not include Markdown syntax such as ```python in the output.

Example:
"""Creates a complex number.

Arguments:
real -- real part (default 0.0)
imag -- imaginary part (default 0.0)

Restrictions:
The number must be an integer"""

Target Code:
{code_content}

Target Function:
{function}
'''

# API call
print("calling API")
response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=prompt_jp
)

# write commented code to the file
# with open (filename, "w", encoding="utf-8") as f:
#     f.write(response.text)
print(response.text)
print("OK")