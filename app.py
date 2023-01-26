from Pext import Pext, request
from Preact.html5 import h1, div, p

app = Pext(__file__, True)

app.head.append({'type': app.loadScript, 'src': 'index.js' })

styles = app.css.load('Home.module.css')


@app.error(404)
def cool(_):
    return [
        {
            'type': h1, 'props': {
                'class': styles.get('title')
            }, 'children': 'hello world'
        },
        {'type': div, 'children': [
            {
                'type': p,
                'children': f'hello world this is a test. you are currently at the path \'{request.path}\''
            }
        ]}
    ]


app.run()
