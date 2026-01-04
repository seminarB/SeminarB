from api import api_call
from analyze import main

def receiveFileAndReturnComment(file):
    ng = main(file)
    result = []

    for name, info in ng.items():
        response = api_call(file, name)
        result.append({
            "line": info["line"],
            "comment": response
        })

    return result

if __name__ == '__main__':
    with open("dummy.py", "r") as f:
        src = f.read()
    result = receiveFileAndReturnComment(src)
    for item in result:
        print(f"📍 {item['line']}行目へのコメント:")
        print(f"{item['comment']}")
        print("-" * 30)