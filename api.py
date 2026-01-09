import sys
import os
from google import genai
from dotenv import load_dotenv # API key (environment variable) is in .env file

def api_call(file, function):
    # read .env file and load variables into the system
    load_dotenv()

    # check if API key was found
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: API key not found.")
        sys.exit(1) # error code

    # the client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client(api_key=api_key)

    code_content = file

    # API call prompt
    # 日本語
    prompt_jp = f'''
    あなたは、以下のPythonコードを作成した経験豊富なプログラマです。
    他の開発者がコードの動作を理解できるように、特定の関数にコメント（docstring）を追加しようとしています。

    指定されたコードの中から「{function}」という名前の関数を見つけ、その機能の要約、引数、戻り値、副作用、送出される例外、および制約事項を記載した複数行のdocstringを作成してください。

    1. Docstringは3つのダブルクォートで開始し、同じ行に関数の概要を記述する
    2. その直後に空行を1つ挿入する
    3. 続いて、引数、戻り値、発生する例外が存在する場合のみ、それぞれ記載する
    4. 値が複合データ構造を持つ場合、例示ではなく値の名称と共にその構造を明記する
    5. 既出の情報から自明ではない場合、必要に応じて制限事項や副作用を記載する
    6. 該当しない項目は記述せず、省略する
    7. 末尾は改行し、3つのダブルクォートで閉じる
    8. 指定された関数がコード内に存在しない場合、空文字のみを返す
    9. コメントは日本語で記述し、動詞は辞書形（基本形）とする
    10. 出力には ```python などのMarkdown記法を含めない
    11. 例外を見れば明らかな制限事項は記載しない
    12. 例示は行わず、発生しうる例外の列挙などの際は、すべての可能性を簡潔に記載する
    13. 引数および戻り値には、変数名に続けて型を記載する
    14. 行末に句点は付けない

    例：
    入力の関数:
    def enchant_wand(wand_type, level=1):
        if level < 1:
            raise ValueError("Enchantment level must be at least 1.")
        return f"{{wand_type.title()}} enchanted to level {{level}}!"

    出力のdocstring:
    """杖に魔法の特性を付与する

    引数:
        wand_type {"x", "y"}: 付与する杖の種類
        level (int, optional): 付与するレベル。デフォルトは 1

    戻り値:
        str: 付与を確認するメッセージ

    送出する例外:
        ValueError: 付与するレベルが無効な場合
    """

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
    3. Then, list arguments, return values, exceptions raised only if they exist respectively. 
    4. When values have composite data structure, explicit along with the name of the value rather than through an example.
    5. List restrictions and side effects if necessary and not obvious from the already inserted information.
    6. Do not describe items that are not applicable; omit them.
    7. In a new line, close with three double quotes at the end.
    8. If the specified function does not exist in the code, return only an empty string.
    9. Write the comment in Japanese, verbs in dictionary form.
    10. Do not include Markdown syntax such as ```python in the output.
    11. Do not add restrictions that are obvious by looking at the exceptions.
    12. Do not use examples; list all possibilities in a brief tone, for example when listing the exceptions raised.
    13. List the name followed by the type of the variables in the arguments and return values.
    14. Leave the end of the lines without a full stop mark.

    Example:
    Input function:
    def enchant_wand(wand_type, level=1):
        if level < 1:
            raise ValueError("Enchantment level must be at least 1.")
        return f"{{wand_type.title()}} enchanted to level {{level}}!"

    Output docstring:
    """杖に魔法の特性を付与する

    引数:
        wand_type {"x", "y"}: 付与する杖の種類
        level (int, optional): 付与するレベル。デフォルトは 1

    戻り値:
        str: 付与を確認するメッセージ

    送出する例外:
        ValueError: 付与するレベルが無効な場合
    """

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
    return response.text

if __name__ == '__main__':
    api_call()