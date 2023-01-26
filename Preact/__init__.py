import json
import re
from .html5 import script, style, DOCTYPE, img, head, body, fragment, UNSAFEHTML
import html


def special_match(strg, search=re.compile(r'[^a-zA-Z0-9.]').search):
    return not bool(search(strg))


class Preact:
    typenamepass = [
        DOCTYPE, UNSAFEHTML
    ]
    cannotselfclose = [script, style, head, body]
    bypassclean = [script, style, UNSAFEHTML]
    doesntclose = [DOCTYPE, img]
    notags = [fragment, UNSAFEHTML]

    def Render(elementdata: dict) -> str:
        if 'props' not in elementdata:
            elementdata['props'] = {}
        if 'children' not in elementdata:
            elementdata['children'] = []
        if callable(elementdata["type"]):
            val = elementdata["type"](elementdata)
            if val:
                return Preact.Render(val)
            return ''
        else:
            output = []
            elementdata["type"] = elementdata["type"].strip()
            if not special_match(elementdata["type"]) and elementdata[
                    "type"] not in Preact.typenamepass:
                raise NameError(
                    'elements cannot have spaces or special charactors in its type!')
            tagname = (elementdata["type"].lower() if elementdata["type"]
                    not in Preact.typenamepass else elementdata["type"])
            if  tagname not in Preact.notags:
                output.append(f'<{tagname}')
                if "props" in elementdata:
                    for props in elementdata["props"]:
                        strippedprops = props.strip()
                        if not strippedprops.isalpha():
                            raise NameError(
                                'setting key cannot have spaces or special charactors in its name!'
                            )
                        if isinstance(elementdata["props"][props], str):
                            elementdata["props"][props] = html.escape(
                                elementdata["props"][props])
                        output.append(
                            f' {strippedprops}={json.dumps(elementdata["props"][props])}'
                        )
            if tagname == DOCTYPE:
                output.append(f' {elementdata["children"]}>')
            elif ("children" in elementdata and
                  (len(elementdata["children"]) > 0 or isinstance(elementdata["children"], dict))) or (tagname
                                                        in Preact.cannotselfclose):
                if tagname not in Preact.notags:
                    output.append(">")
                if "children" in elementdata:
                    if isinstance(elementdata["children"], str):
                        if tagname not in Preact.bypassclean:
                            output.append(html.escape(elementdata["children"]))
                        else:
                            output.append(elementdata["children"])
                    elif isinstance(elementdata["children"], dict):
                        output.append(Preact.Render(elementdata["children"]))
                    else:
                        for child in elementdata["children"]:
                            if not child:
                                pass
                            elif type(child) == dict:
                                output.append(Preact.Render(child))
                            elif tagname not in Preact.bypassclean:
                                output.append(html.escape(child))
                            else:
                                output.append(child)
                if  tagname not in Preact.notags:
                    output.append(f'</{tagname}>')
            elif  tagname not in Preact.notags and tagname not in Preact.doesntclose:
                output.append("/>")
            elif  tagname not in Preact.notags:
                output.append(">")
            return ''.join(output)
