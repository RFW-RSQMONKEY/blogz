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

    def __init__(self, title, body):
        self.title = title
        self.body = body
    
    def __repr__(self):
        return '<Blog %r>' % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def __repr__(self):
        return '<User %r>' % self.email

def get_current_blogs_list():
    return Blog.query.filter_by(blog.id).all()

@app.route('/', methods=['POST', 'GET'])
def index():
    # return get_current_blogs_list
    return render_template('blog.html', title=title, body=body)  
    # return "Hello I am the landing page!"
    # return redirect ('/register.html')




# @app.route('/blog', methods=['POST'])
# def blog():

# @app.before_request
# def require_login():
#    if 'user' not in session and request.endpoint != "login" :
#        return redirect('/login')

# @app.route("/register", methods = ["GET", "POST"])

# def register():
#    if request.method == "POST":
#        #Check out the info, verify it, and redirect
#        #either to errors or to the index page
#        email = request.form["email"]
#        password = request.form["password"]
#        verify = request.form["verify-password"]
#
#        flash("The registration was successful. You are now logged in.")
#        #Add verification to actually register
#        # check if the email is in the database
#        # check if passwords match
#        # check if email is actually and email.
#
#        user = User(email, password)
#        db.session.add(user)
#        db.session.commit()

#        session['user'] = email
#
#        return redirect("/")
    
#    return render_template("register.html")

# @app.route("/validate_user", methods=["POST"])
#def validate_user():
#    username_from_form = request.form["username"]
#    password_from_form = request.form["password"]
#    verify_from_form = request.form["verify"]
#    email_from_form = request.form["email"]

#    username_logic_error = ""
#    password_logic_error = ""
#    verify_logic_error = ""
#    email_logic_error = ""
    
    #username logic
#    if username_from_form == "":
#        username_logic_error="Username must be populated"

#    if len(username_from_form) < 3:
#        username_logic_error = "User name must be longer than 3 and less than 20 characters" 
    
#    if len(username_from_form) >20:
#        username_logic_error = "User name must be longer than 3 and less than 20 characters"
#    
#    if " " in username_from_form:
#        username_logic_error = "Spaces are not allowed in the username" 
#    
    #password logic
#    if password_from_form == "":
#        password_logic_error = "Password must be populated"
#    
#    if " " in password_from_form:
#        password_logic_error = "Spaces are not allowed in the password"
#    
#    if len(password_from_form) < 3:
#        password_logic_error = "User name must be longer than 3 and less than 20 characters" 
#    
#    if len(password_from_form) >20:
#        password_logic_error = "User name must be longer than 3 and less than 20 characters"
#    
#    #verify field logic
#    if verify_from_form =="":
#        verify_logic_error = "Please enter password verification"
#     
#    if " " in verify_from_form:
#        verify_logic_error = "Spaces are not allowed in the password"    
#    
#    if not password_from_form == verify_from_form:
#        verify_logic_error = "Passwords don't match"

    # email logic
    # space or not text handeling
 
#    if " " in email_from_form:
#        email_logic_error = "Spaces are not allowed in the email"       
   
    # length of email and format (requires 1 "@" and 1 ".") 
#    if len(email_from_form) <3:
#        email_logic_error = "Email must be longer than 3 and less than 20 characters" 
#    
#    if len(email_from_form) >20:
#        email_logic_error = "Email must be longer than 3 and less than 20 characters"    
    
#    for char in email_from_form:
#        if email_from_form.count ("@") < 1:
#            email_logic_error = "The email must contain (1) @ and (1) . to be valid"

#        elif email_from_form.count ("@") > 1:
#            email_logic_error = "The email must contain (1) @ and (1) . to be valid"
        
#        else:
#            email_logic_error=""

#    all_error_messages_combined = (username_logic_error + password_logic_error + verify_logic_error + email_logic_error)
#    if all_error_messages_combined == "":
#        return render_template('/login.html", method = 'POST')
#            username=username_from_form)
#    else:
#        return render_template("/register.html", 
#            username=username_from_form, 
#            email=email_from_form, 
#            email_error=email_logic_error,
#            username_error=username_logic_error, 
#            password_error=password_logic_error,
#            verify_error=verify_logic_error) 


# @app.route("/logout", methods = ["POST"])
# def logout():
#    del session['user']
#    return redirect("/")


# @app.route('/newpost', methods=['POST', 'GET'])
# def newpost():
#    if request.method == 'POST':
#        title = request.form['title']
#        new_blog_title = Blog(title)
#        body = request.form['body']
#        new_blog_body = Blog(body)
#        db.session.add(new_blog_title, new_blog_body)
#        db.session.commit()
#    return render_template('blog.html',title=title, body=body)



if __name__ == '__main__':
    app.run()

