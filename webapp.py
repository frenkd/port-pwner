import os

from flask import Flask, render_template, redirect, url_for

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
def event_tracker():
    # Parse query data - specify target
    accountId = request.args.get('target')

    return " "

if __name__ == '__main__':
    app.run(debug=True)
