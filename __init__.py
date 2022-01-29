from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine
import uuid
import kendama_open as ko

app = Flask(__name__)

#tutaj musi iść backendowa obsługa tabel
playerTableLink = 'csv/playerTable.csv'

#HOME
@app.route('/')
def showPlayerTable():
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    dfFin = df[['name', 'surname', 'points', 'word', 'gameUID', 'winGames', 'finGames', 'end']]
    return render_template('base.html', dfDict=dfDict, checkWinner=ko.Game.checkForWinner(dfDict), tables=[dfFin.to_html()], titles=[''])

#CONFIG
@app.route('/changeConfigWord', methods=['POST'])
def changeConfigWord():
    df = ko.Table.show(playerTableLink)
    df['word'] = request.form.get('newWord')
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('showPlayerTable'))

#PLAYER TABLE
@app.route('/addPlayer', methods=['POST'])
def addPlayer():
    name = request.form.get('pName')
    surname = request.form.get('pSurname')
    df = ko.Table.show(playerTableLink)
    dfN = ko.Table.addPlayer(df, [name, surname])
    dfN.to_csv(playerTableLink, mode='a', index=False, header=False)
    return redirect(url_for('showPlayerTable'))

@app.route('/removePlayer/<int:pIndex>', methods=['POST'])
def removePlayer(pIndex):
    df = ko.Table.show(playerTableLink)
    dfN = ko.Table.removePlayer(df, pIndex)
    dfN.to_csv(playerTableLink, index=False)
    return redirect(url_for('showPlayerTable'))

#GAME
@app.route('/addPoint/<int:pIndex>', methods=['POST'])
def addPoint(pIndex):
    df = ko.Game.addPoint(playerTableLink, pIndex)
    dfDict = df.to_dict('records')
    for p in dfDict:
        if p.get('points') == len(p.get('word')):
            p.update({'end':True})
    df = pd.DataFrame(dfDict)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('showPlayerTable'))

@app.route('/removePoint/<int:pIndex>', methods=['POST'])
def removePoint(pIndex):
    df = ko.Game.removePoint(playerTableLink, pIndex)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('showPlayerTable'))

@app.route('/nextGame/<int:gameUID>', methods=['POST'])
def nextGame(gameUID):
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    dfDictN = ko.Game.resetGame(dfDict, gameUID)
    df = pd.DataFrame(dfDictN)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('showPlayerTable'))

if __name__ == "__main__":
    app.run(debug=True)


