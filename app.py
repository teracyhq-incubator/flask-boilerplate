# -*- coding: utf-8 -*-
"""main application entry point"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    """index view page"""
    return '<h1>Hello World!</h1>'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
