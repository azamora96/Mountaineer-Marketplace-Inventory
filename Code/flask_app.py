
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template

app = Flask(__name__, static_url_path="/static")

@app.route('/')
def home():
    return render_template('hw13_home.html')



