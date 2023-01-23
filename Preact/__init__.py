import json
import re
from .html5 import script, style, DOCTYPE, img
import html


def special_match(strg, search=re.compile(r'[^a-zA-Z0-9.]').search):
    return not bool(search(strg))


class Preact:
    typenamepass = [
        DOCTYPE,
    ]
    cannotselfclose = [script]
    bypassclean = [script, style]
    doesntclose = [DOCTYPE, img]

    def Render(elementdata: dict) -> str:
        if callable(elementdata["type"]):
            if 'props' not in elementdata:
                elementdata['props'] = {}
            if 'children' not in elementdata:
                elementdata['children'] = []
            return Preact.Render(elementdata["type"](elementdata))
        else:
            output = []
            elementdata["type"] = elementdata["type"].strip()
            if not special_match(elementdata["type"]) and elementdata[
                    "type"] not in Preact.typenamepass:
                raise NameError(
                    'elements cannot have spaces or special charactors in its type!')
            tagname = (elementdata["type"].lower() if elementdata["type"]
                       not in Preact.typenamepass else elementdata["type"])
            if tagname != '':
                output.append(f'<{tagname}')
                if "props" in elementdata:
                    for props in elementdata["props"]:
                        strippedprops = props.strip()
                        if not strippedprops.isalpha():
                            raise NameError(
                                'setting key cannot have spaces or special charactors in its name!'
                            )
                        output.append(
                            f' {strippedprops}={json.dumps(html.escape(elementdata["props"][props]))}'
                        )
            if tagname == DOCTYPE:
                output.append(f' {elementdata["children"]}>')
            elif ("children" in elementdata and
                  len(elementdata["children"]) > 0) or (tagname
                                                        in Preact.cannotselfclose):
                if tagname != '':
                    output.append(">")
                if "children" in elementdata:
                    for child in elementdata["children"]:
                        if type(child) == dict:
                            output.append(Preact.Render(child))
                        elif tagname not in Preact.bypassclean:
                            output.append(html.escape(child))
                        else:
                            output.append(child)
                if tagname != '':
                    output.append(f'</{tagname}>')
            elif tagname != '' and tagname not in Preact.doesntclose:
                output.append("/>")
            elif tagname != '':
                output.append(">")
            return ''.join(output)
