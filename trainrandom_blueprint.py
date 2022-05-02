from flask import Blueprint
from flask import Flask, session, render_template, request, redirect, url_for

import pandas as pd
import uuid
import kendama_open as ko

trainrandomBlueprint = Blueprint('trainrandom_blueprint', __name__)
trainrandomBlueprint.secret_key = 'gqw5fqw4fg5h577jt7ir68i'

#TRAIN
@trainrandomBlueprint.route('/trainrandom', methods=['POST', 'GET'])
def showTrainMenu():
    return render_template('trainRandom.html')

@trainrandomBlueprint.route('/trainrandom/goback', methods=['POST', 'GET'])
def goback():
    return redirect(url_for('showHome'))