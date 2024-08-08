import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.gui.app import run


def main():
    run()


if __name__ == "__main__":
    main()
