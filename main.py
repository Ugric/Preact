from Preact import Preact
from Preact.html5 import p, h1, hr, style
from flask import Flask, request

app = Flask("__main__")


@app.errorhandler(Exception)
def error(e):
    return Preact.Render({'type':'div','children':[
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
            }]}), 400


app.run(host="0.0.0.0", debug=True)
