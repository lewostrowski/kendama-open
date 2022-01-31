from flask import Flask, render_template, request, redirect, url_for
from game_blueprint import gameBlueprint
from table_blueprint import tableBlueprint
from stats_blueprint import statsBlueprint

import pandas as pd
import uuid

import kendama_open as ko

app = Flask(__name__)
app.register_blueprint(gameBlueprint)
app.register_blueprint(tableBlueprint)
app.register_blueprint(statsBlueprint)

#tutaj musi iść backendowa obsługa tabel
playerTableLink = 'csv/playerTable.csv'
masterLink = 'csv/masterTable.csv'

#HOMES
@app.route('/')
def showHome():
    return render_template('index.html')

@app.route('/startKenGame', methods=['POST', 'GET'])
def startKenGame():
    return redirect(url_for('table_blueprint.showPlayerTable'))

@app.route('/showStats', methods=['POST', 'GET'])
def showStats():
    return redirect(url_for('stats_blueprint.showStats'))

if __name__ == "__main__":
    app.run(debug=True)


