#!/usr/bin/env python3
"""Module of the main ."""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Root route definition."""
    return jsonify({'message': 'bienvenue'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
