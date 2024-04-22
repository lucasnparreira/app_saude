import json
import os
from urllib import response
from flask import Flask, jsonify, render_template, request, redirect, url_for, g
from googlesearch import search
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'
DATABASE = 'database.db'

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
        # Exemplo de dados fictícios (substitua pelos seus dados reais)
    datas = ['2024-04-01', '2024-04-02', '2024-04-03', '2024-04-04']
    pesos = [70, 71, 69, 72]

    # Crie um gráfico de linha usando Google Charts
    chart_data = [['Data', 'Peso']]
    for i in range(len(datas)):
        chart_data.append([datas[i], pesos[i]])
    return render_template('calculate_imc.html',chart_data=chart_data)


@app.route('/healthy_food.html')
def healthy_food():
    # Carregue os dados do arquivo data.json
    with open('templates\data.json', 'r') as arquivo_json:
        dados = json.load(arquivo_json)

        
    return render_template('healthy_food.html', alimentos=dados['proteina_animal'])

# @app.route('/api/data', methods=['GET'])
# def get_data():
#     response = jsonify({'data': 'Dados obtidos com sucesso!'})
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Methods', 'GET')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#     response.headers.add('Access-Control-Allow-Credentials', 'true')

#     return response

# app.static_folder = 'static'

def get_db():
    """
    Retorna uma conexão com o banco de dados.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        # Configurações adicionais, como ativar o suporte a dicionários
        g.db.row_factory = sqlite3.Row
        with app.open_resource('schema.sql', mode='r') as f:
            g.db.cursor().executescript(f.read())
    return g.db

@app.teardown_appcontext
def close_db(error):
    """
    Fecha a conexão com o banco de dados após a solicitação.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/weight_form', methods=['GET', 'POST'])
def weight_tracker():
    if request.method == 'POST':
        weight = request.form['weight']
        date = request.form['date']

        db = get_db()
        db.execute('INSERT INTO weights (weight, date) VALUES (?, ?)', (weight, date))
        db.commit()

    db = get_db()
    weights = db.execute('SELECT * FROM weights ORDER BY date asc').fetchall()

    return render_template('weight_form.html', weights=weights)

@app.route('/delete_weight/<int:weight_id>', methods=['DELETE'])
def delete_weight(weight_id):
    db = get_db()
    db.execute('DELETE FROM weights WHERE id = ?', (weight_id,))
    db.commit()
    return 'Peso excluído com sucesso', 204

if __name__ == '__main__':
    app.run(debug = True)
