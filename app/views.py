from flask import jsonify, redirect, url_for, render_template, request, session, flash
from app import db, app, api
from app.models import User


def loginrequired(func):
    def wrpr(*args, **kwargs):
        if 'user' in session:
            return func(*args, **kwargs)
        else:
            flash(f"Login Required to access this page", "info")
            return redirect(url_for("login"))
    wrpr.__name__ = func.__name__
    return wrpr



@app.route("/home/<name>")
def home(name):
    return render_template("home.html", content=[name.upper(), 'is my name'], x='x')

@app.route("/gethome")
def gethome():
    return render_template("home.html")
    
@app.route('/admin')
@app.route('/admin/make_<name>_admin')
def admin(name='apoorvtyagi'):
    return render_template("admin.html", content=[name.upper(), 'is the admin of this site'], x='go back to login!!')

@app.route("/login", methods=["POST", "GET"])
@app.route("/api/login")
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form['password']
        if isUserpresent(email):
            if authenticateuser(email, password):
                user = User.objects.get(email=email)
                session.permanent = True
                session['user'] = user.email
                session['name'] = user.name
                return redirect(url_for("user"))
            else:
                flash(f"PASSWORD or EMAIL IS(ARE) NOT CORRECT", "info")
                return redirect(url_for("login"))
        else:
            return redirect(url_for("register"))
    else:
        if "user" in session:
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form["register_email"]
        if isUserpresent(email):
            flash(f"YOU ALREADY HAVE AN ACCOUNT TRY LOG IN", "info")
            return redirect(url_for("login"))
        else:
            user = User(name=request.form["register_name"], 
                        email= email,
                        password=request.form['register_password'])
            user.save()
            return redirect(url_for("login"))
    else:
        return render_template("register.html")

    
@app.route('/deactivate', methods=['DELETE'])
def deactivate():
    if 'user' in session:
        user =  User.objects.get(email=session['email'])
        if user:
            user.delete()
        else:
            flash(f"NO DATA FOUND", "info")
    return redirect(url_for("login"))


@app.route('/update', methods=['GET', 'POST'])
@loginrequired
def update():
    user = User.objects.get(email = session['user'])
    if request.method == 'POST':
        update_dic = {
            'name': request.form["update_name"],
            'password': request.form["update_password"]
        }
        user.update(**update_dic)
        user = User.objects.get(email = session['user'])
    return render_template("update.html", objects=user)


@app.route('/showall')
@loginrequired
def showall():
    objects =  User.find()
    return render_template("showall.html", objects=objects)



@app.route("/user")
@loginrequired
def user():
    return redirect(url_for("home", name=session["name"]))




@app.route("/logout")
@loginrequired
def logout():
    session.pop("user", None)
    session.pop("name", None)
    flash(f"YOU HAVE NOT BEEN LOGGED IN", "info")
    return redirect(url_for("login"))



def isUserpresent(email):
    if User.objects.filter(email=email):
        return True
    else:
        return False

def authenticateuser(email, password):
    if password == User.objects.get(email=email).password:
        return True
    return False

# if __name__ == "__main__":
#     app.run(debug=True)
