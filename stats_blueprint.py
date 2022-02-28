from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import uuid
import kendama_open as ko

statsBlueprint = Blueprint('stats_blueprint', __name__)
masterLink = 'csv/masterTable.csv'

@statsBlueprint.route('/showStats')
def showStats():
    df = ko.Table.show(masterLink)
    dfDict = df.to_dict('records')
    uniqueNames = []
    for p in dfDict:
        if p.get('name') not in uniqueNames:
            uniqueNames.append(p.get('name'))
    return render_template('stats.html', dfDict=dfDict, uniqueNames=uniqueNames)

@statsBlueprint.route('/showStats/showGameDetails/<string:masterUID>', methods=['POST', 'GET'])
def showGameDetails(masterUID):
    df = ko.Table.show(masterLink)
    dfN = df.loc[df['masterUID'] == int(masterUID)]
    rounds = []
    for r in dfN['gameUID']:
        if r not in rounds: rounds.append(r)
    dfDict = dfN.to_dict('records')
    
    return render_template('detailedStats.html', dfDict=dfDict, rounds=rounds)

@statsBlueprint.route('/showStats/overallWinner', methods=['POST', 'GET'])
def overallWinner():
    df = ko.Stats.overallWinner(masterLink)
    return render_template('stats.html', dfDict=df['end'])

@statsBlueprint.route('/showStats/masterFilter', methods=['POST', 'GET'])
def timeFilter():
    startDate = request.form.get('startDate')
    endDate = request.form.get('endDate')
    if len(startDate) != '0' or len(endDate) != '0':
        if len(startDate) == 0: startDate = 0
        if len(endDate) == 0: endDate = 0
        df = ko.Stats.filterByDate(masterLink, startDate=startDate, endDate=endDate)
    else:
        df = ko.Table.show(masterLink)

    name = request.form.get('playerName')
    if name != 'all': dfDict = ko.Stats.filterByName(df, name)
    else: dfDict = df.to_dict('records')

    df = ko.Table.show(masterLink)
    dfDrop = df.to_dict('records')
    uniqueNames = []
    for p in dfDrop:
        if p.get('name') not in uniqueNames:
            uniqueNames.append(p.get('name'))
    return render_template('stats.html', dfDict=dfDict, uniqueNames=uniqueNames)

@statsBlueprint.route('/showStats/gameFinish', methods=['POST', 'GET'])
def gameFinish():
    return redirect(url_for('showHome'))
