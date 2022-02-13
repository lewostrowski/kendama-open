from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import uuid
import kendama_open as ko

tableBlueprint = Blueprint('table_blueprint', __name__)
playerTableLink = 'csv/playerTable.csv'
masterLink = 'csv/masterTable.csv'

@tableBlueprint.route('/showPlayerTable')
def showPlayerTable():
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    dfTable = df[['name', 'winGames', 'finGames', 'masterUID']].to_dict()
    return render_template('table.html', dfDict=dfDict, checkWinner=ko.Game.checkForWinner(dfDict), dfTable=dfTable, titles=[''])

#PLAYER TABLE
@tableBlueprint.route('/showPlayerTable/addPlayer', methods=['POST', 'GET'])
def addPlayer():
    name = request.form.get('pName')
    df = ko.Table.show(playerTableLink)
    dfN = ko.Table.addPlayer(df, name)
    dfDict = df.to_dict('records')
    dfDict.append(dfN)
    dfDictN = ko.Game.resetGame(dfDict)
    df = pd.DataFrame(dfDictN)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))

@tableBlueprint.route('/showPlayerTable/removePlayer/<int:pIndex>', methods=['POST', 'GET'])
def removePlayer(pIndex):
    df = ko.Table.show(playerTableLink)
    dfN = ko.Table.removePlayer(df, pIndex)
    if len(dfN) > 0:
        dfDict = dfN.to_dict('records')
        dfDictN = ko.Game.resetGame(dfDict)
        dfN = pd.DataFrame(dfDictN)
    dfN.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))

#CONFIG
@tableBlueprint.route('/showPlayerTable/changeConfigWord', methods=['POST', 'GET'])
def changeConfigWord():
    df = ko.Table.show(playerTableLink)
    df['word'] = request.form.get('newWord')
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))

@tableBlueprint.route('/showPlayerTable/changeConfigMasterUID', methods=['POST', 'GET'])
def changeConfigMasterUID():
    newUID = uuid.uuid4().time
    df = ko.Table.show(playerTableLink)
    df['masterUID'] = newUID
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))

#GAME FUNCTIONS
@tableBlueprint.route('/showPlayerTable/gameFinish', methods=['POST', 'GET'])
def gameFinish():
    df = ko.Table.create()
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('showHome'))
