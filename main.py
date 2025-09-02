from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Rota inicial -> página de login
@app.route('/')
def home():
    return render_template('index.html')

# Rota para cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro1.html')

# Rota para cadastro2
@app.route('/cadastro2')
def cadastro2():
    option = request.args.get('option')  # Obtém a opção selecionada
    return render_template('cadastro2.html', option=option)

# Rota para esqueci a senha
@app.route('/esqueci')
def esqueci():
    return render_template('esqueci.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)