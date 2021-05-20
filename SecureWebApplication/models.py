from datetime import datetime
from SecureWebApplication import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    id = db.Column(db.String(50), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    friends = db.relationship('Friends', backref='User', lazy=True)
    images = db.relationship('Image', backref='User', lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}')"


class Friends(db.Model):

    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.friend_id}')"


class Image(db.Model):

    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    images = db.relationship('Comment', backref='commentOwner', lazy=True)
    image_data = db.Column(db.String(20), nullable=False)
    image_name = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"User('{self.image_data}', '{self.image_name}', '{self.upload_date}')"


class Comment(db.Model):

    id = db.Column(db.String(50), primary_key=True)
    image_id = db.Column(db.String(50), db.ForeignKey('image.id'), nullable=False)
    comment = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"User('{self.comment}')"
