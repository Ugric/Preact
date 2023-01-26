from .html5 import html, body, head, fragment, DOCTYPE


class createTemplate:
    def __init__(self):
        self.__templatehead = []
        self.__firstset = True

    def set(self, headchildren: list):
        if self.__firstset:
            self.__firstset = False
            self.__templatehead = headchildren
        else:
            print(
                "warning: the sethtmltemplatehead function should not be called more then once."
            )

    def use(self, bodychildren):
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
                    "children": self.__templatehead
                }, {
                    "type": body,
                    "children": bodychildren
                }]
            }]
        }
