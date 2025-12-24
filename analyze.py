import subprocess
import csv
import io
import sys
import re

def extract_functions(source, name, length):
    pattern = re.compile(r'^(\s*)def\s+' + name)
    i = 0
    filename = "./tmp/" + name + ".py"
    for i in range(len(source)):
        if pattern.match(source[i]):
            with open(filename, "w") as f:
                for i in range(length+1):
                    f.write(source[i])

def main(filename):
    funcs = []
    result = subprocess.run(
        ["lizard", "--csv", filename],
        capture_output=True,
        text=True
    )
    rows = list(csv.reader(io.StringIO(result.stdout)))
    with open(filename, "r") as f:
        lines = f.readlines()

    with open("list.txt", "w") as f:
        for row in rows:
            nloc = int(row[0])
            ccn = int(row[1])
            token = int(row[2])
            param = int(row[3])
            length = int(row[4])
            file = row[6]
            func = row[7]
            funcs.append(func)
            extract_functions(lines, func, length)

            if ccn <= 10:
                level = "OK"
            else:
                level = "DANGER"
            f.write(f"{func}")

        print(f"{file} {func} CCN={ccn} NLOC={nloc} [{level}]")
    print(funcs)
    return funcs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    main(sys.argv[1])
# https://github.com/terryyin/lizard
# https://github.com/marketplace/actions/lizard-runner