from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import uuid
import kendama_open as ko

gameBlueprint = Blueprint('game_blueprint', __name__)
playerTableLink = 'csv/playerTable.csv'
masterLink = 'csv/masterTable.csv'

#GAME
@gameBlueprint.route('/showGame', methods=['POST', 'GET'])
def showGame():
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    for p in dfDict:
        equalToFirst = dfDict[0].get('word')
        p.update({'word':equalToFirst})
    return render_template('game.html', dfDict=dfDict, checkWinner=ko.Game.checkForWinner(dfDict))

@gameBlueprint.route('/showGame/addPoint/<int:pIndex>', methods=['POST', 'GET'])
def addPoint(pIndex):
    df = ko.Game.addPoint(playerTableLink, pIndex)
    dfDict = df.to_dict('records')
    for p in dfDict:
        if p.get('points') == len(p.get('word')): p.update({'end':True})
    df = pd.DataFrame(dfDict)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('game_blueprint.showGame'))

@gameBlueprint.route('/showGame/removePoint/<int:pIndex>', methods=['POST', 'GET'])
def removePoint(pIndex):
    df = ko.Game.removePoint(playerTableLink, pIndex)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('game_blueprint.showGame'))

@gameBlueprint.route('/showGame/nextGame/<string:masterUID>', methods=['POST', 'GET'])
def nextGame(masterUID):
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    dfMaster = ko.Table.saveToMaster(dfDict)
    if isinstance(dfMaster, pd.DataFrame) == True: dfMaster.to_csv(masterLink, mode='a', index=False, header=False) 
    dfDictN = ko.Game.resetGame(dfDict, masterUID)
    df = pd.DataFrame(dfDictN)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('game_blueprint.showGame'))

@gameBlueprint.route('/showGame/backToHome/<string:masterUID>', methods=['POST', 'GET'])
def backToHome(masterUID):
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')

    dfMaster = ko.Table.saveToMaster(dfDict)
    if isinstance(dfMaster, pd.DataFrame) == True: dfMaster.to_csv(masterLink, mode='a', index=False, header=False) 
    
    isWinner = ko.Game.checkForWinner(dfDict)
    if isWinner == True: 
        dfDictN = ko.Game.resetGame(dfDict, masterUID)
        df = pd.DataFrame(dfDictN)
        df.to_csv(playerTableLink, index=False)
    return redirect(url_for('table_blueprint.showPlayerTable'))