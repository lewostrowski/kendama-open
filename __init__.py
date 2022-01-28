from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine
import kendama_open as ko

app = Flask(__name__)

#tutaj musi iść backendowa obsługa tabel
playerTableLink = 'csv/playerTable.csv'

@app.route('/')
def showPlayerTable():
    df = ko.Table.show(playerTableLink)
    dfDict = df.to_dict('records')
    return render_template('base.html', dfDict=dfDict)


@app.route('/addPlayer', methods=['POST'])
def addPlayer():
    name = request.form.get('pName')
    surname = request.form.get('pSurname')
    df = ko.Table.show(playerTableLink)
    dfN = ko.Table.addPlayer(df, [name, surname])
    dfN.to_csv(playerTableLink, mode='a', index=False, header=False)
    return redirect(url_for('showPlayerTable'))

@app.route('/removePlayer', methods=['POST'])
def removePlayer():
    pIndex = request.form.get('pIndex')
    df = ko.Table.show(playerTableLink)
    dfN = ko.Table.removePlayer(df, pIndex)
    dfN.to_csv(playerTableLink, index=False)
    return redirect(url_for('showPlayerTable'))

@app.route('/addPoint/<int:pIndex>', methods=['POST'])
def addPoint(pIndex):
    df = ko.Game.addPoint(playerTableLink, pIndex)
    df.to_csv(playerTableLink, index=False)
    return redirect(url_for('showPlayerTable'))

if __name__ == "__main__":
    app.run(debug=True)


