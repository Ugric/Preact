from .html5 import html, body, head, fragment, DOCTYPE

templatehead = []
__firstset = True


def sethtmltemplatehead(headchildren: list):
    global templatehead
    global __firstset
    if __firstset:
        __firstset = False
        templatehead = headchildren
    else:
        print(
            "warning: the sethtmltemplatehead function should not be called more then once."
        )


def usehtmltemplate(bodychildren):
    return {
        'type':
        fragment,
        'children': [{
            'type': DOCTYPE,
            'children': 'html'
        }, {
            "type":
            html,
            "children": [{
                "type": head,
                "children": templatehead
            }, {
                "type": body,
                "children": bodychildren
            }]
        }]
    }
