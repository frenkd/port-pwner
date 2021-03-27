import os

from flask import Flask, render_template, redirect, url_for
from portscan import scan
import json

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
      SECRET_KEY='dev',
      )

@app.route('/')
def base():
    return redirect(url_for('home'))

# a simple page that says hello
@app.route('/home')
def home():
    return render_template('home.html', labels=[("Martin", "21"), ("Frenk", "22"), ("Janez", "23")])

@app.route('/scan')
def start_scan():
    accountId = request.args.get('target')
    results = scan(target)
    return json.dumps(results)

if __name__ == '__main__':
    app.run(debug=True)
