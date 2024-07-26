import os
import sys
import time

import flet as ft

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.gui.app import application


def main():
    ft.app(target=application)


if __name__ == "__main__":
    main()
