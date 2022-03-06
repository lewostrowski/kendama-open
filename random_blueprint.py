from flask import Blueprint
from flask import Flask, session, render_template, request, redirect, url_for

import pandas as pd

import kendama_open as ko

randomBlueprint = Blueprint('random_blueprint', __name__)

@randomBlueprint.route('/showRandomMenu')
def showRandomMenu():
    trick = session.get('trick', None)

    return render_template('random.html', trick=trick)

@randomBlueprint.route('/showRandomMenu/pickTrick', methods=['POST', 'GET'])
def pickTrick():
    trick = ko.RandomTricks.pickTrick('/home/user/kendama-open/csv/tricksList/trickTableJapan.csv', 1, 2015)
    session['trick'] = trick
    return redirect(url_for('random_blueprint.showRandomMenu'))

@randomBlueprint.route('/showRandomMenu/gameFinish', methods=['POST', 'GET'])
def gameFinish():
    session.pop('trick')
    return redirect(url_for('showHome'))