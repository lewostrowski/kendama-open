from flask import Flask, render_template, request, redirect, url_for
from game_blueprint import gameBlueprint

import pandas as pd
import uuid

import kendama_open as ko

app = Flask(__name__)
app.register_blueprint(gameBlueprint)

#tutaj musi iść backendowa obsługa tabel
playerTableLink = 'csv/playerTable.csv'
masterLink = 'csv/masterTable.csv'

#HOMES
@app.route('/')
def showPlayerTable():
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    dfFin = df[['name', 'surname', 'points', 'word', 'gameUID', 'winGames', 'finGames', 'end', 'masterUID']]
    return render_template('base.html', dfDict=dfDict, checkWinner=ko.Game.checkForWinner(dfDict), tables=[dfFin.to_html()], titles=[''])

@app.route('/showGame', methods=['POST', 'GET'])
def showGame():
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    for p in dfDict:
        equalToFirst = dfDict[0].get('word')
        p.update({'word':equalToFirst})
    return render_template('game.html', dfDict=dfDict, checkWinner=ko.Game.checkForWinner(dfDict))

@app.route('/showGame/backToHome/<string:masterUID>', methods=['POST', 'GET'])
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
    return redirect(url_for('showPlayerTable'))

#CONFIG
@app.route('/changeConfigWord', methods=['POST', 'GET'])
def changeConfigWord():
    df = ko.Table.show(playerTableLink)
    df['word'] = request.form.get('newWord')
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('showPlayerTable'))

@app.route('/changeConfigMasterUID', methods=['POST', 'GET'])
def changeConfigMasterUID():
    newUID = uuid.uuid4()
    df = ko.Table.show(playerTableLink)
    df['masterUID'] = newUID
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('showPlayerTable'))

#PLAYER TABLE
@app.route('/addPlayer', methods=['POST', 'GET'])
def addPlayer():
    name = request.form.get('pName')
    surname = request.form.get('pSurname')
    df = ko.Table.show(playerTableLink)
    dfN = ko.Table.addPlayer(df, [name, surname])
    dfDict = df.to_dict('records')
    dfDict.append(dfN)
    dfDictN = ko.Game.resetGame(dfDict)
    df = pd.DataFrame(dfDictN)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('showPlayerTable'))

@app.route('/removePlayer/<int:pIndex>', methods=['POST', 'GET'])
def removePlayer(pIndex):
    df = ko.Table.show(playerTableLink)
    dfN = ko.Table.removePlayer(df, pIndex)
    if len(dfN) > 0:
        dfDict = dfN.to_dict('records')
        dfDictN = ko.Game.resetGame(dfDict)
        dfN = pd.DataFrame(dfDictN)
    dfN.to_csv(playerTableLink, index=False)
    return redirect(url_for('showPlayerTable'))

@app.route('/gameFinish', methods=['POST', 'GET'])
def gameFinish():        
    df = ko.Table.create()
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('showPlayerTable'))

if __name__ == "__main__":
    app.run(debug=True)


