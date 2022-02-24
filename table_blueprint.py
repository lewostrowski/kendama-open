from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import uuid
import kendama_open as ko

tableBlueprint = Blueprint('table_blueprint', __name__)
playerTableLink = 'csv/playerTable.csv'
masterLink = 'csv/masterTable.csv'
controlLink = 'csv/gameControl.csv'

@tableBlueprint.route('/showPlayerTable')
def showPlayerTable():
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    if len(df) > 0:
        dfControl = ko.Table.readGameControl(controlLink)
        dfControl = dfControl.to_dict('records')
    else: dfControl = ko.Table.createGameControl(controlLink)
    return render_template('table.html', dfDict=dfDict, checkWinner=ko.Game.checkForWinner(dfDict, dfControl),  dfControl=dfControl)

#PLAYER TABLE
@tableBlueprint.route('/showPlayerTable/addPlayer', methods=['POST', 'GET'])
def addPlayer():
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
    df = ko.Table.show(playerTableLink)
    dfN = ko.Table.removePlayer(df, pIndex)
    dfN.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))

#CONFIG
@tableBlueprint.route('/showPlayerTable/changeConfigWord', methods=['POST', 'GET'])
def changeConfigWord():
    dfControl = ko.Table.readGameControl(controlLink)
    dfControl['word'] = request.form.get('newWord')
    dfControl.to_csv(controlLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))

@tableBlueprint.route('/showPlayerTable/changeConfigMasterUID', methods=['POST', 'GET'])
def changeConfigMasterUID():
    newUID = uuid.uuid4().time
    dfControl = ko.Table.readGameControl(controlLink)
    dfControl['masterUID'] = newUID
    dfControl.to_csv(controlLink, index=False)
    df = ko.Table.show(playerTableLink)
    df['masterUID'] = newUID
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))

@tableBlueprint.route('/showPlayerTable/changeConfigTrunControl', methods=['POST', 'GET'])
def changeConfigTrunControl():
    status = request.form.get('turnControl')
    dfControl = ko.Table.readGameControl(controlLink)
    if status == 'True': dfControl['turnControl'] = True
    else: dfControl['turnControl'] = False
    dfControl.to_csv(controlLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))


#GAME FUNCTIONS
@tableBlueprint.route('/showPlayerTable/gameFinish', methods=['POST', 'GET'])
def gameFinish():
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    # dfMaster = ko.Table.saveToMaster(dfDict)
    # if isinstance(dfMaster, pd.DataFrame) == True: dfMaster.to_csv(masterLink, mode='a', index=False, header=False) 
    df = ko.Table.create()
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('showHome'))
