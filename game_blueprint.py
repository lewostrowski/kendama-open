from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import uuid
import kendama_open as ko

gameBlueprint = Blueprint('game_blueprint', __name__)
playerTableLink = 'csv/playerTable.csv'
masterLink = 'csv/masterTable.csv'
controlLink = 'csv/gameControl.csv'

#GAME
@gameBlueprint.route('/showGame', methods=['POST', 'GET'])
def showGame():
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    dfControl = ko.Table.readGameControl(controlLink)
    dfControl = dfControl.to_dict('records')
    return render_template('game.html', dfDict=dfDict, dfControl=dfControl, checkWinner=ko.Game.checkForWinner(dfDict, dfControl))

@gameBlueprint.route('/showGame/addPoint/<int:pIndex>', methods=['POST', 'GET'])
def addPoint(pIndex):
    df = ko.Game.addPoint(playerTableLink, pIndex)
    dfDict = df.to_dict('records')
    dfControl = ko.Table.readGameControl(controlLink)
    dfControl = dfControl.to_dict('records')
    df = pd.DataFrame(dfDict)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('game_blueprint.showGame'))

@gameBlueprint.route('/showGame/removePoint/<int:pIndex>', methods=['POST', 'GET'])
def removePoint(pIndex):
    df = ko.Game.removePoint(playerTableLink, pIndex)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('game_blueprint.showGame'))

@gameBlueprint.route('/showGame/nextGame/<int:masterUID>', methods=['POST', 'GET'])
def nextGame(masterUID):
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    dfControl = ko.Table.readGameControl(controlLink)
    dfControl = dfControl.to_dict('records')
    if ko.Game.checkForWinner(dfDict, dfControl) == True:
        dfDict = ko.Game.resetGame(dfDict, dfControl)
        df = pd.DataFrame(dfDict)
        df.to_csv(playerTableLink, index=False)
    return redirect(url_for('game_blueprint.showGame'))

@gameBlueprint.route('/showGame/backToHome/<int:masterUID>', methods=['POST', 'GET'])
def backToHome(masterUID):
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    dfControl = ko.Table.readGameControl(controlLink)
    dfControl = dfControl.to_dict('records')
    if ko.Game.checkForWinner(dfDict, dfControl) == True:
        dfDict = ko.Game.resetGame(dfDict, dfControl)
        df = pd.DataFrame(dfDict)
        df.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))