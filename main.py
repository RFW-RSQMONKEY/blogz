from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:123456@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = "Robb_The_Builder_1234"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password
        

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'user_name' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        user=User.query.filter_by(user_name=user_name).first()
        if user and user.password == password:
            session['user_name'] = user_name
            flash ("Logged In")
            return redirect ('/newpost') 
        else:
            flash('User password incorrect, or user does not exist', 'error')
    return render_template('login.html')


@app.route("/register", methods = ['POST' , 'GET'])
def register():
    
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        error_messages = ""
        user_name = request.form['user_name']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(user_name=user_name).first()
        if existing_user:
            flash('Account with this User Name already exists', 'error')
            error_messages += 'e'

        if len(user_name) <3:
            flash("The User Name must be longer than 3 and less than 20 characters", 'error')
            error_messages += 'e' 
 
        if len(user_name) >20:
            flash("The User Name must be longer than 3 and less than 20 characters", 'error')
            error_messages += 'e'    
                 
    #password logic
        if password == "":
            flash("Password must be populated")
            error_messages += 'e'
        if " " in password:
            flash("Spaces are not allowed in the password")
            error_messages += 'e'
        if len(password) < 3:
            flash("User name must be longer than 3 and less than 20 characters")
            error_messages += 'e'
        if len(password) >20:
            flash("User name must be longer than 3 and less than 20 characters")
            error_messages += 'e'
    #verify field logic
        if verify =="":
            flash("Please enter password verification")
            error_messages += 'e'
        if " " in verify:
            flash("Spaces are not allowed in the password")    
            error_messages += 'e'
        if verify != password:
            flash("Passwords don't match")
            error_messages += 'e'
        if error_messages !="":
            return render_template('register.html')    
        if not existing_user:
            new_user = User(user_name, password)
            db.session.add(new_user)
            db.session.commit()
            session['user_name'] = user_name
            return redirect ('/') 
    

@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', blog_users=users)


@app.route('/blog', methods=['POST', 'GET'])
def get_current_blogs_list():
    if request.args.get('id'):
        request_id = request.args.get('id')
        blog_post = Blog.query.filter_by(id=request_id).first()
        user_guy = User.query.filter_by(id=blog_post.owner_id).first()
        return render_template('blogpost.html', post=blog_post, user=user_guy)
    
    if request.args.get('user'):
        user_name = request.args.get('user')
        user_guy = User.query.filter_by(user_name=user_name).first()
        user_id = user_guy.id
        posts = Blog.query.filter_by(owner_id=user_id) 
        return render_template ('blog.html', posts = posts, user=user_guy)
    return render_template ('allblogposts.html', posts=Blog.query.all(), user=User.query.all())


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(user_name = session['user_name']).first()
        new_blog = Blog(title, body, owner)
        db.session.add(new_blog)
        db.session.commit()
        new_blog_id = new_blog.id
        return redirect ('/blog?id=' + str(new_blog_id))
    else:
        return render_template('newpost.html')


@app.route("/logout")
def logout():
    del session['user_name']
    return redirect('/')

if __name__ == '__main__':
    app.run()