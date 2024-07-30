import os
import sys

import flet as ft

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.gui.app import run


def main():
    run()


if __name__ == "__main__":
    main()
