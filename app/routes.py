#verificar hospedagem de site com HostGator Brasil
# verificar PythonAnywhere https://help.pythonanywhere.com/pages/Flask/ 

import json
import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for, g
#from flask_login import LoginManager, UserMixin, current_user, login_required

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'
DATABASE = 'database.db'

template_dir = os.path.abspath('templates')
app.template_folder = template_dir

app.secret_key = 'your_secret_key_here'

#login_manager = LoginManager(app)
# login_manager.login_view = 'login'
#login_manager.login_view = 'weight_tracker'

# Definição da classe User
# class User(UserMixin):
#     def __init__(self, user_id):
#         self.user_id = user_id

# # Função load_user para carregar um usuário com base no ID
# @login_manager.user_loader
# def load_user(user_id):
#     # Substitua esta linha pela lógica real para carregar um usuário do seu banco de dados
#     return User(user_id)

app.config['DATABASE'] = 'database.db'
DATABASE = 'database.db'

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

def get_user_id():
    return session.get('user_id')

@app.route('/weight_form', methods=['GET', 'POST'])
# @login_required
def weight_form():
    user_id = None
    if request.method == 'POST':
        user_id = request.form['user_id']
        weight = request.form['weight']
        date = request.form['date']

        db = get_db()
        db.execute('INSERT INTO weights (user_id, weight, date) VALUES (?, ?, ?)', (user_id, weight, date))
        db.commit()
    
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    return render_template('weight_form.html', users=users)

@app.route('/weight_tracker', methods=['GET'])
#@login_required
def weight_tracker():
        user_id = None
        db = get_db()
        user_id = session.get('user_id')
        # date = request.form['date']
        weights = db.execute('SELECT user_id, date, weight FROM weights WHERE user_id = ? UNION ALL SELECT user_id, date, peso AS weight FROM medidas_corporais WHERE user_id = ? ORDER BY weight ASC, date ASC', (user_id, user_id)).fetchall()
        # weights = db.execute('SELECT * FROM weights WHERE user_id = ? ORDER BY date asc', (user_id,)).fetchall()
        return render_template('weight_tracker.html', weights=weights, user_id = user_id)
    # else:
    #     return redirect(url_for('login'))

# @app.route('/weight_form', methods=['GET', 'POST'])
# #@login_required
# def weight_tracker():
#     user_id = None
#     if request.method == 'POST':
#         user_id = request.form['user_id']
#         weight = request.form['weight']
#         date = request.form['date']

#         db = get_db()
#         db.execute('INSERT INTO weights (user_id, weight, date) VALUES (?, ?, ?)', (user_id, weight, date))
#         db.commit()

#     db = get_db()
#     weights = db.execute('SELECT * FROM weights WHERE user_id = ? ORDER BY date asc', (user_id,)).fetchall()
#     users = db.execute('SELECT * FROM users').fetchall()

#     return render_template('weight_form.html', weights=weights, users=users)


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
            user_id = get_user_id_from_database(username, password)
            session['user_id'] = user_id
            msg = 'Logged in successfully!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username/password!'
            return render_template('login.html', msg=msg)

    return render_template('login.html', msg=msg)

def get_user_id_from_database(username, password):
    """
    Retorna o ID do usuário com base no nome de usuário e senha fornecidos.
    """
    db = get_db()  # Suponha que você já tenha uma função get_db() para obter a conexão com o banco de dados
    user_data = db.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    if user_data:
        return user_data['id']
    else:
        return None  # Retorna None se as credenciais não forem válidas

@app.route('/logout')
def logout():
    session.clear()  # Limpa a sessão do usuário
    return redirect('/')  # Redireciona para a página inicial ou outra página de sua escolha

@app.route('/cadastrar_medidas', methods=['GET', 'POST'])
def cadastrar_medidas():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()

    if request.method == 'POST':
        user_id = request.form['user_id_medidas']
        date = request.form['date']
        altura = request.form['altura']
        peso = request.form['peso']
        circunferencia_cintura = request.form['circunferencia_cintura']
        circunferencia_quadril = request.form['circunferencia_quadril']
        circunferencia_braco = request.form['circunferencia_braco']
        
  
        db = get_db()
        db.execute('INSERT INTO medidas_corporais (user_id, date, altura, peso, circunferencia_cintura, circunferencia_quadril, circunferencia_braco) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, date, altura, peso, circunferencia_cintura, circunferencia_quadril, circunferencia_braco))
        db.commit()
        return redirect(url_for('cadastrar_medidas'))

    # Se for uma requisição GET, simplesmente renderize a página HTML
    return render_template('body_check.html', users=users)

@app.route('/cadastro_sucesso')
def cadastro_sucesso():
    return "Medidas corporais cadastradas com sucesso!"

@app.route('/exibir_medidas', methods=['GET'])
# @login_required
def exibir_medidas():
    user_id = None
    db = get_db()
    user_id = session.get('user_id')
    # pesos = db.execute('SELECT user_id, date, weight as peso FROM weights WHERE user_id = ? UNION ALL SELECT user_id, date, peso AS mc FROM medidas_corporais WHERE user_id = ? ORDER BY peso ASC, date ASC', (user_id,user_id)).fetchall()
    medidas = db.execute('SELECT * FROM medidas_corporais where user_id = ? ORDER BY date ASC', (user_id,)).fetchall()
    return render_template('exibir_medidas.html', medidas=medidas, user_id = user_id)

@app.route('/excluir_medidas/<int:medidas_id>', methods=['DELETE'])
#@login_required
def excluir_medidas(medidas_id):
    db = get_db()
    db.execute('DELETE FROM medidas_corporais WHERE id = ?', (medidas_id,))
    db.commit()
    return 'Medidas excluídas com sucesso', 204

from flask import jsonify

@app.route('/get_medidas_data/<item>', methods=['GET'])
def get_medidas_data(item):
    # Verifique se o item é válido para evitar injeção de SQL
    valid_items = ['peso', 'altura', 'date', 'circunferencia_braco','circunferencia_quadril','circunferencia_cintura']  # Adicione outros itens conforme necessário
    if item not in valid_items:
        return jsonify({'error': 'Item inválido'}), 400

    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    db = get_db()
    medidas = db.execute(f"SELECT date, {item} FROM medidas_corporais WHERE user_id = ? ORDER BY date ASC", (user_id,)).fetchall()
    data = [{'date': row['date'], item: row[item]} for row in medidas]

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug = True)
