from flask import Blueprint
from flask import Flask, session, render_template, request, redirect, url_for

import pandas as pd
import uuid
import shutil

import kendama_open as ko

tableBlueprint = Blueprint('table_blueprint', __name__)
tableBlueprint.secret_key = 'gqw5fqw4fg5h577jt7ir68i'

@tableBlueprint.route('/showPlayerTable')
def showPlayerTable():
    playerTableLink = session.get('playerTable', None)
    controlLink = session.get('gameControl', None)
    try:
        df = ko.Table.show(playerTableLink)
    except:
        df = ko.Table.show(0)
        df.to_csv(playerTableLink, index=False)

    dfDict = df.to_dict('records')
    if len(df) > 0:
        dfControl = ko.Table.readGameControl(controlLink)
        dfControl = dfControl.to_dict('records')
    else: 
        dfControl = ko.Table.createGameControl(controlLink)
        dfControl = dfControl.to_dict('records')
    return render_template('table.html', dfDict=dfDict, checkWinner=ko.Ken.checkForWinner(dfDict, dfControl),  dfControl=dfControl)

#PLAYER TABLE
@tableBlueprint.route('/showPlayerTable/addPlayer', methods=['POST', 'GET'])
def addPlayer():
    playerTableLink = session.get('playerTable', None)
    name = request.form.get('pName')
    df = ko.Table.show(playerTableLink)
    n = set(df['name'])
    if name not in n:
        dfN = ko.Table.addPlayer(df, name)
        dfDict = df.to_dict('records')
        dfDict.append(dfN)
        df = pd.DataFrame(dfDict)
        df.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))

@tableBlueprint.route('/showPlayerTable/removePlayer/<int:pIndex>', methods=['POST', 'GET'])
def removePlayer(pIndex):
    playerTableLink = session.get('playerTable', None)
    df = ko.Table.show(playerTableLink)
    dfN = ko.Table.removePlayer(df, pIndex)
    dfN.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))

#CONFIG
@tableBlueprint.route('/showPlayerTable/changeConfigWord', methods=['POST', 'GET'])
def changeConfigWord():
    controlLink = session.get('gameControl', None)
    dfControl = ko.Table.readGameControl(controlLink)
    dfControl['word'] = request.form.get('newWord')
    dfControl.to_csv(controlLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))

@tableBlueprint.route('/showPlayerTable/changeConfigMasterUID', methods=['POST', 'GET'])
def changeConfigMasterUID():
    playerTableLink = session.get('playerTable', None)
    controlLink = session.get('gameControl', None)
    newUID = uuid.uuid4().time
    dfControl = ko.Table.readGameControl(controlLink)
    currentMasterUID = 0
    for masterUID in dfControl['masterUID']:
        currentMasterUID = dfControl.loc[dfControl['masterUID'] == masterUID].values[0][0]
    if currentMasterUID == 0: dfControl['masterUID'] = newUID
    else: dfControl['masterUID'] = 0
    dfControl.to_csv(controlLink, index=False)
    df = ko.Table.show(playerTableLink)
    df['masterUID'] = newUID
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))

@tableBlueprint.route('/showPlayerTable/changeConfigTrunControl', methods=['POST', 'GET'])
def changeConfigTrunControl():
    controlLink = session.get('gameControl', None)
    status = request.form.get('turnControl')
    dfControl = ko.Table.readGameControl(controlLink)
    if status == 'True': dfControl['turnControl'] = True
    else: dfControl['turnControl'] = False
    dfControl.to_csv(controlLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))


#GAME FUNCTIONS
@tableBlueprint.route('/showPlayerTable/gameFinish', methods=['POST', 'GET'])
def gameFinish():
    contestDirectory = session.get('contesDir', None)
    shutil.rmtree(contestDirectory)
    return redirect(url_for('showHome'))
