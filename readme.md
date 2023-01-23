# Preact

Preact is a small hobby project that aims to replicate the functionality of React in Python. It allows developers to create and render UI components using a JSX-like syntax and a virtual DOM, making it easy to create dynamic and interactive user interfaces.

## Installation

this package is not currently on pip

## Usage

Here's an example of how to use the Preact package to render a simple button component:

```python
from Preact import Preact
from Preact.html5 import button


def MyButton(element):
    return {
        "type": button,
        "props": {"className": "my-button", "onClick": element['props']['onclick']},
        "children": element["children"],
    }


button = Preact.Render(
    {'type': MyButton, 'props': {'onclick': "alert('Button clicked!')"}})
print(button)
```

The above code will output the following HTML:

```html
<button className="my-button" onClick="alert(&#x27;Button clicked!&#x27;)">
    Click Me!
</button>
```

## Contributing

If you're interested in contributing to the Preact package, please feel free to fork the repository and submit a pull request.

## License

This project is licenced under the MIT Licence - see the [LICENCE](LICENCE) file for details
