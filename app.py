from flask import Flask, request, render_template, redirect,flash, session ,json,jsonify
from models import db, connect_db, User, Post, Tag
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] ="oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)
"""db.drop_all()
db.create_all()"""
 
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
   

@app.route("/users/<int:user_id>/posts/new",methods=["GET"])
def show_form_to_add_a_post  (user_id):
  userid = user_id
  user = User.query.get_or_404(user_id)
  user_name = f"{user.first_name} {user.last_name}"
  tags =  tags = Tag.query.all()
  return render_template("postform.html",userid=userid, user_name = user_name, tags =tags) 

@app.route("/users/<int:user_id>/posts/new",methods=["POST"])
def add_post  (user_id):
  tittle = request.form['tittle']
  content = request.form['content']
  tags = request.form.getlist('tags')
  tagList =[]

  for tag_id in tags:
      tag = Tag.query.get_or_404(tag_id)
      tagList.append(tag)
  post = Post(tittle=tittle, content=content, user_id=user_id, tags = tagList)
  db.session.add(post)
  db.session.commit()
  print(f"Post  created  with id {post.id}")
  user = User.query.get_or_404(user_id)
  return render_template("userdetail.html", user=user) 

@app.route("/posts/<int:post_id>",methods=["GET"])
def show_post  (post_id):
   post = Post.query.get_or_404(post_id)
   return render_template("showpost.html", post=post) 

@app.route("/posts/<int:post_id>/edit",methods=["GET"])
def show_post_edit  (post_id):
   post = Post.query.get_or_404(post_id)
   tags = Tag.query.all()
   return render_template("postedit.html", post=post, tags =tags) 

@app.route("/posts/<int:post_id>/edit",methods=["POST"])
def edit_post  (post_id):
   post = Post.query.get_or_404(post_id)
   post.tittle = request.form['tittle']
   post.content = request.form['content']
   tags = request.form.getlist('tags')
   tagList =[]

   for tag_id in tags:
      tag = Tag.query.get_or_404(tag_id)
      tagList.append(tag)
 
   post.tags = tagList
   db.session.add(post)
   db.session.commit()
   user = User.query.get_or_404(post.user_id)
   flash(f"Post id  {post.id} has  been updated", 'success')
   return render_template("userdetail.html", user=user)


@app.route("/posts/<int:post_id>/delete",methods=["POST"])
def delete_post  (post_id):
    """Delete a Postr."""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post id  {post_id} has  been deleted", 'success')
    return render_template("userdetail.html", user=user)


@app.route("/tags",methods=["GET"])
def list_all_tags ():
   """List all tags"""
   tags =Tag.query.all()
   return render_template("tags.html", tags=tags)

@app.route("/tags/<int:tag_id>",methods=["GET"])
def show_tag_detail  (tag_id):
   tag = Tag.query.get_or_404(tag_id)
   return render_template("viewtag.html", tag=tag)

@app.route("/tags/new",methods=["GET"])
def create_a_tag_get  ():
    tags = Tag.query.all()
    return render_template("createtag.html", tags = tags)

@app.route("/tags/new",methods=["POST"])
def create_a_tag_post  ():
    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    flash(f"Tag {tag.name} has  been created", 'success')
    return redirect(f"/tags")

@app.route("/tags/<int:tag_id>/edit",methods=["GET"])
def edit_tag_get (tag_id):
   tag = Tag.query.get_or_404(tag_id)
   return render_template("edittag.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit",methods=["POST"])
def edit_tag_Post (tag_id):
   print("I am in edit tag")
   tag = Tag.query.get_or_404(tag_id)
   name = request.form['name']
   tag.name = name;
   db.session.add(tag)
   db.session.commit()
   flash(f"Tag {tag.name} has  been edited", 'success')
   return redirect(f"/tags")

@app.route("/tags/<int:tag_id>/delete",methods=["POST"])
def delete_tag  (tag_id):
    """Delete a tag."""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Post id  {tag_id} has  been deleted", 'success')
    return redirect(f"/tags")



