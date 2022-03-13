from os import defpath
from flask import Blueprint
from flask import Flask, session, render_template, request, redirect, url_for

import pandas as pd

import kendama_open as ko

randomBlueprint = Blueprint('random_blueprint', __name__)

@randomBlueprint.route('/showRandomMenu')
def showRandomMenu():
    tricksControl = session.get('tricksControl', False)
    if tricksControl != True: session['tricksControl'] = False

    tricksHistory = session.get('tricksHistory', [])
    if len(tricksHistory) == 0: session['tricksHistory'] = []

    years = ['2014', '2015', '2016', '2017', '2018', '2019']
    levels = ['1','2','3','4','5','6','7','8','9','10']

    trick = session.get('trick', [])
    previousYears = session.get('previousYears', [])
    previousLevels = session.get('previousLevels', [])

    df = ko.RandomTricks.readTable('csv/tricksList/tickList.csv')
    return render_template('random.html', trick=trick, years=years, levels=levels, previousYears=previousYears, previousLevels=previousLevels)

@randomBlueprint.route('/showRandomMenu/pickTrick', methods=['POST', 'GET'])
def pickTrick():
    years = ['2014', '2015', '2016', '2017', '2018', '2019']
    inputYears = []
    for y in years:
        year = request.form.get(y)
        if year is not None: inputYears.append(y)

    levels = ['1','2','3','4','5','6','7','8','9','10']
    inputLevels = []
    for l in levels:
        lvl = request.form.get(l)
        if lvl is not None: inputLevels.append(l)

    if len(inputYears) == 0: inputYears = years
    if len(inputLevels) == 0: inputLevels = levels
    trick = ko.RandomTricks.pickTrick('csv/tricksList/tickList.csv', inputLevels, inputYears)

    if session.get('tricksControl') == True:
        avalibelTricks = (len(inputLevels)*10)*len(inputYears)
        if len(session.get('tricksHistory')) < avalibelTricks:
            while trick[0].get('name') in session.get('tricksHistory'):
                trick = ko.RandomTricks.pickTrick('csv/tricksList/tickList.csv', inputLevels, inputYears)
            
            session['trick'] = trick
            session['previousYears'] = inputYears
            session['previousLevels'] = inputLevels
            session['tricksHistory'].append(trick[0].get('name'))
        else: 
            session['END'] = True
    else:        
        session['trick'] = trick
        session['previousYears'] = inputYears
        session['previousLevels'] = inputLevels
    return redirect(url_for('random_blueprint.showRandomMenu'))

@randomBlueprint.route('/showRandomMenu/deselectYears', methods=['POST', 'GET'])
def deselectYears():
    session.pop('previousYears')
    return redirect(url_for('random_blueprint.showRandomMenu'))

@randomBlueprint.route('/showRandomMenu/deselectLevels', methods=['POST', 'GET'])
def deselectLevels():
    session.pop('previousLevels')
    return redirect(url_for('random_blueprint.showRandomMenu'))

@randomBlueprint.route('/showRandomMenu/tricksControl', methods=['POST', 'GET'])
def tricksControl():
    currentStatus = session.get('tricksControl', False)
    if currentStatus == False:
        session['tricksControl'] = True
    else: 
        session['tricksControl'] = False
    return redirect(url_for('random_blueprint.showRandomMenu'))

@randomBlueprint.route('/showRandomMenu/reset', methods=['POST', 'GET'])
def reset():
    session['tricksHistory'] = []
    session['END'] = False
    session['trick'] = []
    return redirect(url_for('random_blueprint.showRandomMenu'))

@randomBlueprint.route('/showRandomMenu/gameFinish', methods=['POST', 'GET'])
def gameFinish():
    try:
        session.pop('trick')
        session.pop('tricksHistory')
        session.pop('END')
    except:
        print('No trick to delete')

    try:
        session.pop('previousYears')
        session.pop('previousLevels')
    except:
        print('EOL')

    session.pop('tricksControl')
    return redirect(url_for('showHome'))