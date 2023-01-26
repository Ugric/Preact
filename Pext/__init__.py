import sys
import os
from flask import *
from css_html_js_minify.js_minifier import remove_commented_lines, js_minify_keep_comments
from typing import Union

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from css_modules import css_module
from Preact import Preact
from Preact.createtemplate import createTemplate
from Preact.html5 import style, fragment, script


def js(code: str) -> str:
    code = remove_commented_lines(code)
    code = js_minify_keep_comments(code)
    return code.strip()


def loadFromCSSModule(props):
    module: css_module = props['props']['module']
    render = module.render()
    if render:
        return {'type': style, 'children': render}
    return None


class Pext:
    def __init__(self, currentpath: str, dev=False):
        self.dirname = os.path.dirname(currentpath)
        self.css = css_module(currentpath)
        self.template = createTemplate()
        self.head = []
        self.template.set([
            {'type': loadFromCSSModule, 'props': {'module': self.css}},
            {'type': fragment, 'children': self.head},
        ])
        self.dev = dev
        self.scriptcache: dict[str, str] = {}

        self.flask = Flask(__name__)

    def loadScript(self, props):
        path = os.path.join(self.dirname, props['props']['src'])
        if 'elementProps' not in props['props']:
            props['props']['elementProps'] = {}
        if path not in self.scriptcache:
            file = open(path, 'r')
            read = file.read()
            file.close()
            self.scriptcache[path] = js(read)
        code = self.scriptcache[path]
        return {'type': script, 'props': props['props']['elementProps'], 'children': code}

    def render(self, elements: Union[dict, str, list]) -> str:
        return Preact.Render(self.template.use(elements))
    def __tupilise(self, resp) -> tuple:

        if not isinstance(resp, tuple):
            resp = (resp, 200)
        if isinstance(resp[0], str) or isinstance(resp[0], list) or isinstance(resp[0], dict):
            resp = list(resp)
            resp[0] = self.render(resp[0])
            resp = tuple(resp)
        return resp
    def page(self, rule, **options):
        def p(func: str):
            @self.flask.route(rule, **options)
            def _(**vals):
                return self.__tupilise(func(**vals))
        return p

    def error(self, code_or_exception):
        def p(func: str):
            @self.flask.errorhandler(code_or_exception)
            def _(e):
                return self.__tupilise(func(e))
        return p


    def run(self, host = None, port = None, load_dotenv: bool = True, **options):
        self.flask.run(host, port, self.dev, load_dotenv, **options)
