from flask import Flask, request, render_template, redirect,flash, session ,json,jsonify
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] ="oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)

@app.route("/")
def home_page():
  users =User.query.all()
  print("hello")
  return render_template("homepage.html",users =users)

@app.route("/createuser")
def create_user():
  return render_template("user.html")

@app.route("/createuser", methods=["POST"])
def add_user():
  print ("I am in post create user")
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  image = request.form['image']
  user = User(first_name=first_name, last_name=last_name, image=image)
  db.session.add(user)
  db.session.commit()
  print(f"User Id created is {user.id}")
  return redirect(f"/showuser/{user.id}")

@app.route("/showuser/<int:user_id>")
def show_user(user_id):
    """Show info on a single User."""
    user = User.query.get_or_404(user_id)
    return render_template("userdetail.html", user=user)

@app.route("/delete/",methods=["DELETE"])
def delete_user():
    """Delete a single User."""
    user_id = int(json.loads(request.data)["user_id"])
    print(f"User id {user_id}")
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "Success"

@app.route("/update/<int:user_id>",methods=["GET"])
def update_user (user_id):
   user = User.query.get_or_404(user_id)
   return render_template("updateuser.html", user=user)


@app.route("/update/<int:user_id>",methods=["POST"])
def update_user_post (user_id):
  user = User.query.get_or_404(user_id)
  user.first_name = request.form['first_name']
  user.last_name = request.form['last_name']
  user.image = request.form['image']
  db.session.add(user)
  db.session.commit()
  flash(f"User {user.first_name} {user.last_name} has  been updated", 'success')
  return render_template("userdetail.html", user=user)
   

