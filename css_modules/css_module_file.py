import re
import random
import string
import os
from css_html_js_minify import css_minify


def _randstr(str_size=12):
    return ''.join(random.choice(string.ascii_letters) for _ in range(str_size))


classnametest = re.compile(r'\.-?[_a-zA-Z]+[_a-zA-Z0-9-]*')


class css_module_file:
    def __init__(self, filename: str):
        file = open(filename, 'r')
        self.raw = file.read()
        file.close()
        self.name = os.path.basename(filename).split('.')[0]
        self.classes = [e[1:]
                        for e in (sorted(set(classnametest.findall(self.raw))))]
        self.newAssignment = {}
        self.css = self.raw
        for i in range(len(self.classes)):
            c = self.classes[i]
            newcname = f'{self.name}_{c}__{_randstr(5)}'
            self.css = self.css.replace(f'.{c}', f'.{newcname}')
            self.newAssignment[c] = newcname
        self.css = css_minify(self.css, comments=False, noprefix=True)

    def get(self, classname: str) -> str:
        if classname in self.newAssignment:
            return self.newAssignment[classname]
        print('Error: class name', classname, 'does not exist. defaulting to an empty string.')
        return ''
