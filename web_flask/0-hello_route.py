#!/usr/bin/python3
"""returns hello script"""
from flask import Flask
import os

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    hello function
    """
    return "Hello HBNB!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
