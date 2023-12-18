from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User (db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=True)
    image = db.Column(db.String(400), nullable=False)
    post = db.relationship('Post')

class Post(db.Model):
     """Post"""
     __tablename__ = "posts"
     id =  db.Column(db.Integer, primary_key=True,autoincrement=True)
     tittle = db.Column(db.String(300), nullable=False)
     content = db.Column(db.String(800), nullable=False)
     created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
     user_id = db.Column( db.Integer, db.ForeignKey('users.id'))
     user = db.relationship('User')
     tags = db.relationship('Tag',secondary='post_tags',backref='posts')
    


class PostTag(db.Model):
    """PostTag"""
    __tablename__ = "post_tags"
    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer,db.ForeignKey("tags.id"), primary_key=True)

class Tag (db.Model):
    """Tag"""
    __tablename__ = "tags"
    id =  db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(300),unique =True ,nullable=False)
  