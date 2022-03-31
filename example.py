from Preact import Preact
from Preact.createtemplate import usehtmltemplate, sethtmltemplatehead
from Preact.html5 import p, h1, hr, style
from flask import Flask, request

app = Flask("__main__")

sethtmltemplatehead([{
    "type":
    style,
    "children":
    """
body {
  font-family: Arial, Helvetica, sans-serif;
}
"""
}])


@app.errorhandler(404)
def error(e):
    return Preact.Render(
        usehtmltemplate([
          {
            "type": h1,
            "children": request.path
        }, {
            "type": hr
        }, {
            "type":
            p,
            "children":
            "this script wont run: <script>console.log('hello world!')</script> which is good!"
        }]))


app.run(host="0.0.0.0", debug=True)
