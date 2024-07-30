import importlib
import importlib.resources
import os

import flet as ft

from lia.gui.app import application

if __name__ == "__main__":
    path = importlib.resources.files("lia")
    ft.app(target=application, assets_dir=str(path) + "/assets")
