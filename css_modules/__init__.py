import os
from .css_module_file import css_module_file


class css_module:
    def __init__(self, currentpath: str):
        self.dirname = os.path.dirname(currentpath)
        self.css_modules: dict[str, css_module_file] = {}

    def load(self, path: str) -> css_module_file:
        fullpath = os.path.join(self.dirname, path)
        if fullpath in self.css_modules:
            return self.css_modules[fullpath]
        load = css_module_file(fullpath)
        self.css_modules[fullpath] = load
        return load

    def render(self) -> str:
        output = []
        for path in self.css_modules:
            load = self.css_modules[path]
            output.append(load.css)
        return ''.join(output)