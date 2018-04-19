from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Robb1@localhost:8889/build-a-blog'
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

    def __repr__(self):
        return '<Blog %r>' % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password, owner):
        self.email = email
        self.password = password
        
    
    def __repr__(self):
        return '<User %r>' % self.email

def get_current_blogs_list():
    return Blog.query.filter_by(blog.id).all()

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user=User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash ("Logged In")
            
            return redirect ('/') 
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


@app.route("/register", methods = ['POST' , 'GET'])
def register():
    existing_user = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        if existing_user == User.query.filter_by(email=email).first():
            flash("Account with this email already exists")
            return redirect ('/register')

        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect ('/')

        if " " in email:
            flash("Spaces are not allowed in the email")       
    
        if len(email) <3:
            flash("Email must be longer than 3 and less than 20 characters") 
 
        if len(email) >20:
            flash("Email must be longer than 3 and less than 20 characters")    
        
        for char in email:
            if email.count ("@") < 1:
                flash ("The email must contain (1) @ and (1) . to be valid")
            
            elif email.count ("@") > 1:
                flash = "The email must contain (1) @ and (1) . to be valid"
    
            else:
                email=""
    #password logic
        if password == "":
            flash ("Password must be populated")
        
        if " " in password:
            flash ("Spaces are not allowed in the password")
       
        if len(password) < 3:
            flash ("User name must be longer than 3 and less than 20 characters")
       
        if len(password) >20:
            flash ("User name must be longer than 3 and less than 20 characters")
        
    #verify field logic
        if verify =="":
            flash = "Please enter password verification"
        
        if " " in verify:
            flash ("Spaces are not allowed in the password")    
        
        if verify != password:
            flash ("Passwords don't match")
        
#    all_error_messages_combined = (username_logic_error + password_logic_error + verify_logic_error + email_logic_error)
        if all_error_messages_combined == "":
            return render_template('login.html', email=email)
        else:
            return render_template('register.html', 
                email=email, 
                password=password,
                verify=verify) 
    return render_template('register.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('blog.html')  


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'POST':
        title =title
        
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect ("/")
    else:
        return render_template('newpost.html')


@app.route("/logout")
def logout():
    del session['email']
    return redirect('/')

if __name__ == '__main__':
    app.run()