from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User (db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(100),
                     nullable=False)
    last_name = db.Column(db.String(100), nullable=True)
    image = db.Column(db.String(400), nullable=False)