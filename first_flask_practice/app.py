from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
#from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

bootstrap = Bootstrap(app)



# configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
#mysql.init_app(app)
#print(db)


@app.route('/')
def index():
     cur = mysql.connection.cursor()
     #cur.execute('''CREATE TABLE example (id INTEGER, name VARCHAR(20))''')
     #cur.execute('''INSERT INTO example VALUES(1,'Morenikeji')''')
     #cur.execute('''INSERT INTO example VALUES(2,'Ayomide')''')
     
     if cur.execute('''INSERT INTO example VALUES (3, 'Motune')'''):
         mysql.connection.commit()   
         return 'success', 201
     #users = cur.fetchall()
     #print(users)
     #return 'Done!'
     #return users[0]['name']
     return render_template('index.html')
    #fruits = ['Apple', 'Mango', 'Orange']
    #return render_template('index.html',fruits=fruits)
    #return redirect(url_for('about'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/css')
def css():
    return render_template('css.html')


@app.errorhandler(404)
def page_not_found(e):
    return 'This page was not found!'

if __name__ == '__main__':
    app.run(debug=True)
