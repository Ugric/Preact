import json
import bleach
import re


def special_match(strg, search=re.compile(r'[^a-zA-Z0-9.]').search):
    return not bool(search(strg))


class Preact:
    typenamepass = [
        "!DOCTYPE",
    ]

    def Render(elementdata: dict):
        if (callable(elementdata["type"])):
            return Preact.Render(elementdata["type"](elementdata))
        else:
            output = ""
            elementdata["type"] = elementdata["type"].strip()
            if not special_match(elementdata["type"]) and elementdata[
                    "type"] not in Preact.typenamepass:
                raise NameError(
                    'elements cannot have spaces or special charactors in its type!'
                )
            tagname = (elementdata["type"].lower() if elementdata["type"]
                       not in Preact.typenamepass else elementdata["type"])
            output += f'<{tagname}'
            if "settings" in elementdata:
                for setting in elementdata["settings"]:
                    strippedsettings = setting.strip()
                    if not strippedsettings.isalpha():
                        raise NameError(
                            'setting key cannot have spaces or special charactors in its name!'
                        )
                    output += f' {strippedsettings}={json.dumps(elementdata["settings"][setting])}'
            if "children" in elementdata and len(elementdata["children"]) > 0:
                output += ">"
                for child in elementdata["children"]:
                    if type(child) == dict:
                        output += Preact.Render(child)
                    else:
                        output += bleach.clean(child)
                output += f'</{tagname}>'
            else:
                output += "/>"
            return output
