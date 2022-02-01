from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import uuid
import kendama_open as ko

statsBlueprint = Blueprint('stats_blueprint', __name__)
playerTableLink = 'csv/playerTable.csv'
masterLink = 'csv/masterTable.csv'

@statsBlueprint.route('/showStats')
def showStats():
    df = ko.Table.show(masterLink)
    dfDict = df.to_dict('records')
    dfFin = df[['name', 'points', 'word', 'gameUID', 'winGames', 'finGames', 'end', 'masterUID', 'timestamp']]
    return render_template('stats.html', dfDict=dfDict, tables=[dfFin.to_html()], titles=[''])

@statsBlueprint.route('/showStats/overallWinner', methods=['POST', 'GET'])
def overallWinner():
    df = ko.Stats.overallWinner(masterLink)
    return render_template('stats.html', dfDict=df['end'])