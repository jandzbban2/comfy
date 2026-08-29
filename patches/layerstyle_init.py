import importlib
import os
import sys

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

py = os.path.join(os.path.dirname(__file__), "py")
if os.path.exists(py):
    for file in sorted(os.listdir(py)):
        if not file.endswith(".py"):
            continue
        name = os.path.splitext(file)[0]
        try:
            m = importlib.import_module(".py." + name, __name__)
            if hasattr(m, "NODE_CLASS_MAPPINGS"):
                NODE_CLASS_MAPPINGS.update(m.NODE_CLASS_MAPPINGS)
            if hasattr(m, "NODE_DISPLAY_NAME_MAPPINGS"):
                NODE_DISPLAY_NAME_MAPPINGS.update(m.NODE_DISPLAY_NAME_MAPPINGS)
        except Exception as e:
            print(f"[LayerStyle] Note: submodule '{file}' skipped ({e})")

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
