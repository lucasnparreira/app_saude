import json
import os
from urllib import response
from flask import Flask, jsonify, render_template, request, redirect, url_for
from googlesearch import search

import requests

app = Flask(__name__)
template_dir = os.path.abspath('templates')
app.template_folder = template_dir

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercise_tips')
def exercise_tips():
    return render_template('exercise_tips.html')

@app.route('/calculate_imc', methods=['GET','POST'])
def calculate_imc():
    # if request.method == 'POST':
    #     weight = float(request.form['weight'])
    #     height = float(request.form['height'])
    #     bmi = calculate_bmi(weight,height)
    # imc_result = IMCResult(weight = weight, height = height, bmi = bmi)
    # db.session.add(imc_result)
    # db.session.commit()

    return render_template('calculate_imc.html')

# def calculate_bmi(weight, height):
#     return weight / (height ** 2)

@app.route('/healthy_food.html')
def healthy_food():
    # Carregue os dados do arquivo data.json
    with open('templates\data.json', 'r') as arquivo_json:
        dados = json.load(arquivo_json)
    return render_template('healthy_food.html', alimentos=dados['proteina_animal'])

@app.route('/api/data', methods=['GET'])
def get_data():
    # Sua lógica para obter dados

    # Configuração dos cabeçalhos CORS
    response = jsonify({'data': 'Dados obtidos com sucesso!'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Credentials', 'true')

    return response

app.static_folder = 'static'

if __name__ == '__main__':
    app.run(debug = True)
