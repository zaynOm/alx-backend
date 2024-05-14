#!/usr/bin/env python3
"""Basic Falsk app"""

from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def hello():
    """Hello world route"""
    return render_template("0-index.html")
