"""
Ovo rješenje je više-manje kopija rješenja koje sam predao prošle godine, ali
implementirano u pythonu, a ne u javi.
"""

import sys


def main():
    if sys.argv[1] == "resolution":
        pass

    elif sys.argv[1] == "cooking":
        pass

    else:
        raise Exception("The program only supports 'resolution' and 'cooking'")


if __name__ == "__main__":
    main()
