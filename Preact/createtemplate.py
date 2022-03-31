from .html5 import html, body, head
templatehead = []
_firstset = True
def sethtmltemplatehead(headchildren):
  global templatehead
  global _firstset
  if _firstset:
    _firstset = False
    templatehead = headchildren
  else:
    raise ValueError("the sethtmltemplatehead function cannot be called more then once.")
def usehtmltemplate(bodychildren):
  return {"type": html, "children": [{"type": head, "children": templatehead}, {"type": body, "children": bodychildren}]}