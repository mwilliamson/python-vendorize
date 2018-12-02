import re


def find_encoding(fileobj):
    for line_index in range(0, 2):
        line = fileobj.readline()
        # From PEP 263
        match = re.match(br"^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)", line)
        if match is not None:
            return match.group(1).decode("ascii")

    return "utf-8"
