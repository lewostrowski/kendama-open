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
    for p in dfDict:
        if p.get('points') == len(dfControl[0].get('word')): p.update({'winner':True})
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
    dfControl = ko.Table.readGameControl(controlLink)
    dfControl = dfControl.to_dict('records')
    dfDict = df.to_dict('records')
    dfDictN = ko.Game.resetGame(dfDict, dfControl)
    df = pd.DataFrame(dfDictN)
    df.to_csv(playerTableLink, index=False)
    print(df)
    return redirect(url_for('game_blueprint.showGame'))

@gameBlueprint.route('/showGame/backToHome/<int:masterUID>', methods=['POST', 'GET'])
def backToHome(masterUID):
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')

    # dfMaster = ko.Table.saveToMaster(dfDict)
    # if isinstance(dfMaster, pd.DataFrame) == True: dfMaster.to_csv(masterLink, mode='a', index=False, header=False) 

    dfControl = ko.Table.readGameControl(controlLink)
    dfControl = dfControl.to_dict('records')

    isWinner = ko.Game.checkForWinner(dfDict, dfControl)
    if isWinner == True: 
        dfDictN = ko.Game.resetGame(dfDict, dfControl, nextGame=True)
        df = pd.DataFrame(dfDictN)
        df.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))