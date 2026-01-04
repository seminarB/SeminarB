from api import api_call
from analyze import main

def receiveFileAndReturnComment(file):
    ng = main(file)
    result = []

    for name, info in ng.items():
        response = api_call(file, name)
        result.append({
            "line": info["lineno"],
            "comment": response
        })

    return result

if __name__ == '__main__':
    with open("api.py", "r") as f:
        src = f.read()
    print(receiveFileAndReturnComment(src))