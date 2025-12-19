import subprocess
import csv
import io
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    filename = sys.argv[1]
    result = subprocess.run(
        ["lizard", "--csv", filename],
        capture_output=True,
        text=True
    )
    rows = list(csv.reader(io.StringIO(result.stdout)))

    for row in rows:
        nloc = int(row[0])
        ccn = int(row[1])
        token = int(row[2])
        param = int(row[3])
        file = row[6]
        func = row[7]

        if ccn <= 10:
            level = "OK"
        else:
            level = "DANGER"

        print(f"{file} {func} CCN={ccn} NLOC={nloc} [{level}]")
# https://github.com/terryyin/lizard
# https://github.com/marketplace/actions/lizard-runner