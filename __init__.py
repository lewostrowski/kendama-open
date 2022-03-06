from flask import Flask, session, render_template, request, redirect, url_for
from game_blueprint import gameBlueprint
from table_blueprint import tableBlueprint
from stats_blueprint import statsBlueprint
from random_blueprint import randomBlueprint

import pandas as pd
import uuid
import os

import kendama_open as ko

app = Flask(__name__)
app.register_blueprint(gameBlueprint)
app.register_blueprint(tableBlueprint)
app.register_blueprint(statsBlueprint)
app.register_blueprint(randomBlueprint)

# sKey = str(uuid.uuid1())
app.secret_key = 'gqw5fqw4fg5h577jt7ir68i'

#HOMES
@app.route('/')
def showHome():
    return render_template('index.html')

@app.route('/startKenGame', methods=['POST', 'GET'])
def startKenGame():
    sessionUID = uuid.uuid4().hex
    sessionUIDStr = str(sessionUID)
    dir = os.path.join('csv', sessionUIDStr)
    os.mkdir(dir)
    session['playerTable'] = os.path.join(dir, 'playerTable.csv')
    session['gameControl'] = os.path.join(dir, 'gameControl.csv')
    session['contesDir'] = dir
    return redirect(url_for('table_blueprint.showPlayerTable'))

@app.route('/randomTrick', methods=['POST', 'GET'])
def randomTrick():
    return redirect(url_for('random_blueprint.showRandomMenu'))

@app.route('/showStats', methods=['POST', 'GET'])
def showStats():
    return redirect(url_for('stats_blueprint.showStats'))

if __name__ == "__main__":
    app.run(debug=True)
