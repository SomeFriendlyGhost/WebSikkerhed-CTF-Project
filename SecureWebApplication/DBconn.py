import base64
import datetime
import uuid
import io
import os
import secrets
from SecureWebApplication import db, models, bcrypt, app


def registerUser(Firstname, Lastname, Email, Password):

    user = models.User(id=str(uuid.uuid4()) ,firstname=Firstname, lastname=Lastname, email=Email, password=Password)
    db.session.add(user)
    db.session.commit()


def getUser(Email, Password):
    user = models.User.query.filter_by(email=Email).first()
    if user and bcrypt.check_password_hash(user.password, Password):
        return user


def addFriend(Id, Email):
    to_be_friend = models.User.query.filter_by(email=Email).first()
    friend = models.Friends(id=str(uuid.uuid4()), user_id=Id, friend_id=to_be_friend.id)
    print(friend)
    db.session.add(friend)
    db.session.commit()

def getPictures(user_id):
    friendlist = models.Friends.query.filter(models.Friends.user_id == user_id).all()
    image_list = []
    for friend in friendlist:
        image_list = models.Image.query.filter_by(user_id=friend.friend_id).all()
    return image_list


def uploadImage(imagedata, user_id):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(imagedata.filename)
    picture_filename = f_name + f_ext
    #picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_filename)
    imagedata.save(picture_path)
    timestamp = datetime.datetime.today()
    image = models.Image(id=str(uuid.uuid4()), user_id=user_id, image_data=picture_path, image_name=picture_filename, upload_date=timestamp)
    print(image)
    db.session.add(image)
    db.session.commit()


def uploadComment(imageid, commentdata):
    comment = models.Comment(id=str(uuid.uuid4()), image_id=imageid, comment=commentdata)
    db.session.add(comment)
    db.session.commit()

def getComments(imageid):
    comment_list = models.Comment.query.filter(models.Comment.image_id == imageid).all()
    for comment in comment_list:
        eval(comment.comment)
    return comment_list