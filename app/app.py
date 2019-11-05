from flask import Flask, request, render_template
app = Flask(__name__)
application = app
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/log')
def log():
    return render_template('log.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run()