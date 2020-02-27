from flask import current_app, Flask, g
import mysql.connector

class MySQL():
    def __init__(self, app, **connect_args): #конструктор класса
        self.connector = mysql.connector #создание коннектора
        self.connect_args = connect_args # создание объекта для конфигов
        self.app = app
        self.app.teardown_appcontext(self.close_db) #закрытие БД  
        
    
    def connection(self): # подключение к самой БД если ее нет в глобальном объекте
        if 'db' not in g: 
            g.db = self.connect()
        return g.db

    def connect(self): #подключение к БД
        self.config()
        return mysql.connector.connect(**self.connect_args) #возвращает подключение коннектора к БД

    def config(self): # забитие настроечек из конфига
        self.connect_args['host'] = self.app.config.get('MYSQL_DATABASE_HOST', 'localhost')
        self.connect_args['port'] = self.app.config.get('MYSQL_DATABASE_PORT', 3306)
        self.connect_args['user'] = self.app.config.get('MYSQL_DATABASE_USER')
        self.connect_args['password'] = self.app.config.get('MYSQL_DATABASE_PASSWORD')
        self.connect_args['db'] = self.app.config.get('MYSQL_DATABASE_DB')
     
    def close_db(self, e=None): #закрытие БД
        db = g.pop('db', None)
        if db is not None:
            db.close()

