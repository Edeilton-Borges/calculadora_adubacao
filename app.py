from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "chave_secreta_segura"  # Protege a sessão do usuário

# Defina um usuário e senha padrão
USUARIO = "admin"
SENHA = "1234"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == USUARIO and senha == SENHA:
            session['logado'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro="Usuário ou senha incorretos")

    return render_template('login.html')

@app.route('/index')
def index():
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('login'))

@app.route('/calcular_adubacao', methods=['POST'])
def calcular_adubacao():
    if not session.get('logado'):
        return redirect(url_for('login'))

    area = float(request.form['area'])
    necessidade = float(request.form['necessidade'])
    composicao = float(request.form['composicao'])

    if composicao > 0:
        quantidade_fertilizante = (necessidade / (composicao / 100)) * area
    else:
        quantidade_fertilizante = 0

    return render_template('index.html', resultado_adubacao=quantidade_fertilizante)

@app.route('/calcular_fitossanitario', methods=['POST'])
def calcular_fitossanitario():
    if not session.get('logado'):
        return redirect(url_for('login'))

    area_fito = float(request.form['area_fito'])
    dosagem = float(request.form['dosagem'])

    total_produto = area_fito * dosagem

    return render_template('index.html', resultado_fitossanitario=total_produto)

if __name__ == '__main__':
    app.run(debug=True)
