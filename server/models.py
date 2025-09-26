from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from marshmallow import Schema, fields

# Import the db instance from config instead of creating a new one
from config import db

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)
    preview = db.Column(db.String)
    minutes_to_read = db.Column(db.Integer)
    is_member_only = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'content': self.content,
            'preview': self.preview,
            'minutes_to_read': self.minutes_to_read,
            'is_member_only': self.is_member_only,
            'date': self.date.isoformat() if self.date else None
        }

    def __repr__(self):
        return f'Article {self.id} by {self.author}'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)

    articles = db.relationship('Article', backref='user')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def __repr__(self):
        return f'User {self.username}, ID {self.id}'

class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()

    articles = fields.List(fields.Nested(lambda: ArticleSchema(exclude=("user",))))

class ArticleSchema(Schema):
    id = fields.Int()
    author = fields.String()
    title = fields.String()
    content = fields.String()
    preview = fields.String()
    minutes_to_read = fields.Int()
    is_member_only = fields.Boolean()
    date = fields.DateTime()

    user = fields.Nested(UserSchema(exclude=("articles",)))