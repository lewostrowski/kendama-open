from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for

import pandas as pd

import kendama_open as ko

randomBlueprint = Blueprint('random_blueprint', __name__)

@randomBlueprint.route('/showRandomMenu')
def showRandomMenu():
    return render_template('random.html')

@randomBlueprint.route('/showRandomMenu/gameFinish', methods=['POST', 'GET'])
def gameFinish():
    return redirect(url_for('showHome'))