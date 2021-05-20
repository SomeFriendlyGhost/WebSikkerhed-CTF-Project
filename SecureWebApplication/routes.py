from SecureWebApplication import DBconn, app, forms, bcrypt
from flask import redirect, url_for, render_template, flash, request
from flask_login import login_user, current_user


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data, 5).decode('utf-8')
        DBconn.registerUser(form.firstname.data, form.lastname.data, form.email.data, hashed_pw)
        return redirect(url_for('login'))
    return render_template('register.html',  form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    print('test1')
    if form.validate_on_submit():
        print('test2')
        user = DBconn.getUser(form.email.data, form.password.data)
        if user:
            print(user.email, user.firstname)
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('login unsuccessful')
    return render_template('login.html',  form=form)


@app.route('/Home', methods=['GET', 'POST'])
def home():
    UploadPictureForm = forms.UploadPictureForm()
    image_list = DBconn.getPictures(current_user.get_id())
    if UploadPictureForm.submit.data and UploadPictureForm.validate():
        DBconn.uploadImage(UploadPictureForm.picture.data, current_user.get_id())

    return render_template('Home.html', image_list=image_list, UploadPictureForm=UploadPictureForm)


@app.route('/Friends', methods=['GET', 'POST'])
def friends():
    form = forms.AddFriendForm()
    if form.validate_on_submit():
        DBconn.addFriend(current_user.get_id(), form.email.data)
    return render_template('Friends.html', form=form)

@app.route('/Comment', methods=['GET', 'POST'])
def comment():
    form = forms.UploadCommentForm()
    image_name = request.args.get('filename')
    image_id = request.args.get('id')
    comment_list =DBconn.getComments(image_id)
    if form.validate_on_submit():
        DBconn.uploadComment(form.image_id.data, form.comment.data)
    return render_template('comment.html', form=form, image_name=image_name, image_id=image_id, comment_list=comment_list)
