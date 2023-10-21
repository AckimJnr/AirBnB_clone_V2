#!/usr/bin/python3
"""returns hello script"""
from flask import Flask
from markupsafe import escape


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    hello function
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    prints hbnb
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    prints c followed by variable text
    """
    formated_text = text.replace('_', ' ')
    return f'C {escape(formated_text)}'


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python/')
def python_text(text='is cool'):
    formated_text = text.replace('_', ' ')
    return f'Python {escape(formated_text)}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)