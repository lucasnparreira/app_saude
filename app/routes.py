#verificar hospedagem de site com HostGator Brasil

import json
import os
from urllib import response
from flask import Flask, jsonify, render_template, request, redirect, session, url_for, g
from googlesearch import search
import sqlite3
# from flask_login import login_required
#from flask_login import LoginManager

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'
DATABASE = 'database.db'



app = Flask(__name__)
template_dir = os.path.abspath('templates')
app.template_folder = template_dir

#app.config.from_pyfile = 'app\config.py'
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercise_tips')
#@login_required
def exercise_tips():
    return render_template('exercise_tips.html')

@app.route('/calculate_imc', methods=['GET','POST'])
#@login_required
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
#@login_required
def healthy_food():
    # Carregue os dados do arquivo data.json
    with open('templates\data.json', 'r') as arquivo_json:
        dados = json.load(arquivo_json)

        
    return render_template('healthy_food.html', alimentos=dados['proteina_animal'])


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
#@login_required
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
#@login_required
def delete_weight(weight_id):
    db = get_db()
    db.execute('DELETE FROM weights WHERE id = ?', (weight_id,))
    db.commit()
    return 'Peso excluído com sucesso', 204


@app.route('/register', methods=['GET', 'POST'])
#@login_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        number_id = request.form['number_id']
        date = request.form['date']
        password = request.form['password']

        db = get_db()
        db.execute('INSERT INTO users (username, number_id, date, password) VALUES (?, ?, ?, ?)',
                   (username, number_id, date, password))
        db.commit()

        return redirect(url_for('login'))  # Redireciona para a página de login após o registro bem-sucedido

    return render_template('register.html')  # Exibe o formulário de registro


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username/password!'
            return render_template('login.html', msg=msg)

    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.clear()  # Limpa a sessão do usuário
    return redirect('/')  # Redireciona para a página inicial ou outra página de sua escolha

if __name__ == '__main__':
    app.run(debug = True)
