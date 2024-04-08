import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, IMCResult

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

def calculate_bmi(weight, height):
    return weight / (height ** 2)

@app.route('/healthy_food.html')
def healthy_food():
    return render_template('healthy_food.html')

@app.route('/api/food_info', methods = ['POST'])
def food_info():
    food_name = request.json.get('food')
    app_id = ''
    app_key = ''

    request = requests.get(f'https://api.nutritionix.com/v1_1/search/{food_name}?results=0%3A1&fields=item)name%2Citem_id%2Cbrand_name%2Cnf_calories%2Cnf_total_fat%2Cnf_protein%2Cnf_total_carbohydrate&appId={app_id}&appkey={app_key}')

    if response.status_code == 200:
        data = response.json()
        if data['hits']:
            food = data['hits'][0]['fields']
            food_info = {
                'name' : food['item_name'],
                'calories' : food['nf_calories'],
                'total_fat' : food['nf_total_fat'],
                'protein' : food['nf_protein'],
                'total_carbohydrate' : food['nf_total_carbohydrate']
            }

            return jsonify(food_info), 200
        else:
            return jsonify({'error':'Alimento nao encontrado.'}), 404
    else:
        return jsonify({'error':'Erro ao buscar informacoes nutricionais.'}), 500


app.static_folder = 'static'

if __name__ == '__main__':
    app.run(debug = True)
