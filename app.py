from flask import Flask, request, redirect, g, render_template, session, jsonify
import genetique as gen
import recuit_simule as recuit
import tabou as tabou
app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html',range_4=range(4), range_10= range(10))

if __name__ == '__main__':
    app.run(debug=True)