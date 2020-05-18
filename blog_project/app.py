from flask import Flask, render_template, flash, session, request, redirect
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ckeditor import CKEditor
import yaml
import os


app = Flask(__name__)
Bootstrap(app)
ckeditor =CKEditor(app)

# configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24)



@app.route('/')
def index():
    cur = mysql.connection.cursor()
    resultValue = cur.execute('SELECT * FROM blog')
    if resultValue >0:
        blogs = cur.fetchall()
        cur.close()
        return render_template('index.html', blogs=blogs)
    cur.close()
    return render_template('index.html', blogs=None)


@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/blogs/<int:id>/')
def blogs(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute('SELECT * FROM blog WHERE blog_id ={}'.format(id))
    if resultValue > 0:
        blog = cur.fetchone()
        return render_template('blogs.html', blog=blog)
    return 'Blog not found'

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('register.html')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(first_name, last_name, user_name, email, password) "\
        "VALUES(%s,%s,%s,%s,%s)",(userDetails['first_name'], userDetails['last_name'], \
        userDetails['user_name'], userDetails['email'], userDetails['password']))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.', 'success')
        return redirect('/login')
    return render_template('register.html')

@app.route('/login/', methods = ['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         userDetails = request.form
#         username = userDetails['user_name']
#         cur = mysql.connection.cursor()
#         resultValue = cur.execute('SELECT * FROM user WHERE user_name = %s', ([username]))
#         if resultValue > 0:
#             user = cur.fetchone()
#             if check_password_hash(user['password'] == userDetails['password']):
#                 session['login'] = True
#                 session['firstName'] = user['first_name']
#                 session['lastName'] = user['last_name']
#                 flash('Welcome' + session['firstName'] + '! You have been successfully logged in', 'success')
#             else:
#                 cur.close()
#                 flash('Password does not match', 'danger')
#                 return render_template('login.html')
#         else:
#             cur.close()
#             flash('User not found', 'danger')
#             return render_template('login.html')
#         cur.close()
#         return redirect('/')
#     return render_template('login.html')
def login():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['user_name']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM user WHERE user_name = %s", ([username]))
        if resultValue > 0:
            user = cur.fetchone()
            if userDetails['password'] == user['password']:
                session['login'] = True
                session['firstName'] = user['first_name']
                session['lastName'] = user['last_name']
                flash('Welcome ' + session['firstName'] +'! You have been successfully logged in', 'success')
            else:
                cur.close()
                flash('Password does not match', 'danger')
                return render_template('login.html')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login.html')
        cur.close()
        return redirect('/')
    return render_template('login.html')

@app.route('/write-blog/', methods = ['GET', 'POST'])
def write_blog():
    if request.method =='POST':
        blogpost = request.form
        title = blogpost['title']
        body = blogpost['body']
        author = session['firstName'] +' ' + session['lastName']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO blog(title, body,blog) VALUES(%s,%s,%s)', (title,body,author))
        mysql.connection.commit()
        cur.close()
        flash('Successfully posted a new blog', success)
        return redirect('/')
    return render_template('write-blog.html')

@app.route('/my-blogs/')
def my_blogs():
    author = session['firstName'] + ' ' + session['lastName']
    cur = mysql.connection.cursor()
    resultValue = cur.execute('SELECT * FROM blog WHERE author = %s',[author])
    if resultValue > 0:
        my_blogs = cur.fetchall()
        return render_template('my-blogs.html', my_blogs=my_blogs)
    return render_template('my-blogs.html', my_blogs=None)

@app.route('/edit-blog/<int:id>/', methods = ['GET', 'POST'])
def edit_blog():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        title = request.form['title']
        body = request.form['body']
        cur.execute('UPDATE blog SET title = %s, body=%s WHERE blog_id = %s',(title,body,id))
        mysql.connection.commit()
        cur.close()
        flash('Blog updated successfully', success)
        return redirect('/blogs/{}'.format(id))
    cur = mysql.connection.cursor()
    resultValue = cur.execute('SELECT * FROM blog WHERE blog_id ={}'.format(id))
    if resultValue >0:
        blog = cur.fetchone()
        blog_form = {}
        blog_form['title'] = blog['title']
        blog_form['body'] = blog['body']
        return render_template('edit-blog.html',blog_form=blog_form)

@app.route('/delete-blog/<int:id>', methods= ['POST'])
def delete_blog(id):
    cur =mysql.connection.cursor()
    cur.execute('DELETE FROM blog WHERE blog_id = {}'.format(id))
    mysql.connection.commit()
    flash('Your blog has been deleted successfully', success)
    return redirect('/my-blogs')

@app.route('/logout')
def logout():
    session.clear()
    flash('you have been logged out','info')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5001)