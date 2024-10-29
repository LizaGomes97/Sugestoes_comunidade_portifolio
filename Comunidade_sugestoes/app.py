from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key= 'sua_chave_secreta'

#conectando ao banco de dados
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='comunidade_sugestoes'
    )
    return connection

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        hashed_senha = generate_password_hash(senha, method='sha256')#criptografa minha senha

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('INSERT INTO usuarios(nome,email,senha) VALUES (%s,%s,%s)', (nome,email,hashed_senha))
            connection.commit()
            flash('Usuário registrado com sucesso!')
            return redirect (url_for('home'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}')
        finally:
            cursor.close()
            connection.close()
    return render_template('register.html')
    
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        connection = get_db_connection()
        cursor= connection.cursor()

        cursor.execute('SELECT senha FROM usuarios WHERE email =%s', (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[0], senha):
            flash('Login bem-sucedido!')
            return redirect (url_for('home'))
        else:
            flash('Email ou senha incorretos')
        cursor.close()
        connection.close()

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
