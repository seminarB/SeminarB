from api import api_call
from analyze import main

def receiveFileAndReturnComment(file):
    ng = main(file)
    result = []

    for name, info in ng.items():
        response = api_call(info["original_src"])
        result.append({
            "line": info["line"],
            "comment": response
        })

    return result

if __name__ == '__main__':
    with open("pbl.py", "r") as f:
        src = f.read()
    result = receiveFileAndReturnComment(src)
    with open("text.txt", "w") as f:

        for item in result:
            f.write(f"📍 {item['line']}行目へのコメント:")
            f.write(f"{item['comment']}")
            f.write("-" * 30)