from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for


aboutBlueprint = Blueprint('about_blueprint', __name__)
aboutBlueprint.secret_key = 'gqw5fqw4fg5h577jt7ir68i'

@aboutBlueprint.route('/showAbout', methods=['POST', 'GET'])
def showAbout():
    return render_template('about.html')

@aboutBlueprint.route('/showAbout/goback', methods=['POST', 'GET'])
def goback():
    return redirect(url_for('showHome'))