from flask import Blueprint
from flask import Flask, session, render_template, request, redirect, url_for

import pandas as pd
import uuid
import kendama_open as ko

gameBlueprint = Blueprint('game_blueprint', __name__)
gameBlueprint.secret_key = 'gqw5fqw4fg5h577jt7ir68i'

#GAME
@gameBlueprint.route('/showGame', methods=['POST', 'GET'])
def showGame():
    playerTableLink = session.get('playerTable', None)
    controlLink = session.get('gameControl', None)
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    dfControl = ko.Table.readGameControl(controlLink)
    dfControl = dfControl.to_dict('records')
    return render_template('game.html', dfDict=dfDict, dfControl=dfControl, checkWinner=ko.Ken.checkForWinner(dfDict, dfControl))

@gameBlueprint.route('/showGame/addPoint/<int:pIndex>', methods=['POST', 'GET'])
def addPoint(pIndex):
    playerTableLink = session.get('playerTable', None)
    df = ko.Ken.addPoint(playerTableLink, pIndex)
    dfDict = df.to_dict('records')
    df = pd.DataFrame(dfDict)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('game_blueprint.showGame'))

@gameBlueprint.route('/showGame/removePoint/<int:pIndex>', methods=['POST', 'GET'])
def removePoint(pIndex):
    playerTableLink = session.get('playerTable', None)
    df = ko.Ken.removePoint(playerTableLink, pIndex)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('game_blueprint.showGame'))

@gameBlueprint.route('/showGame/nextGame/<int:masterUID>', methods=['POST', 'GET'])
def nextGame(masterUID):
    playerTableLink = session.get('playerTable', None)
    controlLink = session.get('gameControl', None)
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    dfControl = ko.Table.readGameControl(controlLink)
    dfControl = dfControl.to_dict('records')
    if ko.Ken.checkForWinner(dfDict, dfControl) == True:
        dfDict = ko.Ken.resetGame(dfDict, dfControl, controlLink)
        df = pd.DataFrame(dfDict)
        df.to_csv(playerTableLink, index=False)
    return redirect(url_for('game_blueprint.showGame'))

@gameBlueprint.route('/showGame/backToHome/<int:masterUID>', methods=['POST', 'GET'])
def backToHome(masterUID):
    playerTableLink = session.get('playerTable', None)
    controlLink = session.get('gameControl', None)

    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    dfControl = ko.Table.readGameControl(controlLink)
    dfControl = dfControl.to_dict('records')
    if ko.Ken.checkForWinner(dfDict, dfControl) == True:
        dfDict = ko.Ken.resetGame(dfDict, dfControl, controlLink)
        df = pd.DataFrame(dfDict)
        df.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))