from flask import Flask, request, render_template, session, redirect, url_for, g, flash
import flask_login
from flask_login import current_user
from DB import MySQL
import mysql.connector as connector

app = Flask(__name__)
app.secret_key = b'YidceDBlXG55b0tuP1FceGYyXHgwNy5EXHhjNlx4OTRceGI4UycK'
app.config.from_pyfile('config.py')
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
mysql=MySQL(app)
application = app

class User(flask_login.UserMixin):
	pass

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/log')
def log():
    return render_template('log.html')

@app.route('/auth', methods=['GET', 'POST']) #авторизация для админов
def auth():
    if request.method == 'GET':
        return render_template('auth.html')
      
    username = request.form.get('login')
    password = request.form.get('password')
    error = 'введите логин и пароль'

    if username and password:
        cursor = mysql.connection().cursor(named_tuple=True)
        cursor.execute('select id, login, status from users where login = %s and password = %s',(username, password))
        user_from_db=cursor.fetchone()
        if user_from_db:
            user=User()
            user.id=user_from_db.id
            user.login=user_from_db.login
            flask_login.login_user(user, remember=True)
            next = request.args.get('next')
            if next:
                error = "успешно"
                return render_template("auth.html", error=error)
                #return redirect(next)
            else:
                error = "успешно"
                return render_template("auth.html", error=error)           
                #return redirect(url_for('home'))
        else:
            error='Неверный логин или пароль'
            return render_template("auth.html", error=error)
    return render_template("auth.html", error=error)

@app.route('/home') #главная админская страница
@flask_login.login_required
def home():
    return render_template('homePage.html')

@login_manager.user_loader  # загрузка пользователя из куки
def user_loader(id): 
    cursor=mysql.connection().cursor(named_tuple=True) 
    cursor.execute('select * from users where id = %s;', (id,))
    user_from_db=cursor.fetchone()
    if user_from_db:
        user = User()
        user.id = user_from_db.id
        user.login = user_from_db.login
        return user 
    return None

@app.before_request
def before_request():
    g.user = current_user


@app.route ('/newPage', methods=['GET', 'POST']) #создание новой страницы
@flask_login.login_required
def newPage():
    if request.method == 'POST': 
        return render_template('admin.html')
    
    else:
        pathToTemplates = '/templates/'
        page = request.form.get('newPage')
        nameOfpage = request.form.get('nameOfPage')
        # по хорошему сделать проверку от перезаписи, проверка через базу. 
        # 
        nameOfPage = pathToTemplates+nameOfPage
        with io.open(nameOfPage, 'w') as f:
            f.write(page)
        f.close()
        flash('страница добавлена')
        return redirect(url_for('home'))
        

@app.route ('/editPage', methods=['GET', 'POST']) #перенаправление на редактирование страницы
@flask_login.login_required
def edit():
    if request.method == 'GET':
        return render_template('edit.html')

@app.route('/page/<int:id>/edit', methods=['GET', 'POST']) #редактирование страницы
@flask_login.login_required
def editPage():
    pass

@app.route('/page/<int:id>/delete', methods=['GET', 'POST']) #удаление страницы
@flask_login.login_required
def deletePage():
    pass

@app.route('/page/<int:id>', methods=['GET', 'POST']) #открытие страниц
def getPage(id):
    return render_template('index.html', id=id)

if __name__ == '__main__':
    app.run()
