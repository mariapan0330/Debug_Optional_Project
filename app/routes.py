from app import app, Message, mail
from flask import render_template, request, redirect, url_for, flash

# Import for Forms
from app.forms import UserInfoForm, PostForm, LoginForm

# Import for Models
from app.models import User, Post

# Import for Flask Login - login_required, login_user,current_user, logout_user
from flask_login import login_required, login_user, current_user, logout_user

# Home Route
@app.route('/')
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)

# Register Route
@app.route('/register', methods=['GET','POST'])
def register():
    form = UserInfoForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Get Information
        username = form.username.data
        password = form.password.data
        email = form.email.data
        print("\n",username,password,email)
        # Create an instance of User
        user = User(username=username,email=email,password=password)

        # Flask Email Sender 
        msg = Message(f'Thanks for Signing Up! {email}', recipients=[email])
        msg.body = ('Congrats on signing up! Looking forward to your posts!')
        msg.html = ('<h1> Welcome to debug_project_app!</h1>' '<p> This will be fun! </p>')
        return redirect(url_for('login'))
        # mail.send(msg)
    return render_template('register.html',form=form)

# Post Submission Route
@app.route('/posts', methods=['GET','POST'])
@login_required
def posts():
    post = PostForm()
    if request.method == 'POST' and post.validate_on_submit():
        title = post.title.data
        content = post.content.data
        print('\n',title,content)
        post = Post(title=title,content=content,user_id=current_user.id)
        return redirect(url_for('post_detail', post_id = post.id))
    return render_template('posts.html', post = post)

@app.route('/posts/<post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post = post)


@app.route('/posts/update/<post_id>', methods = ['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    update_form = PostForm()

    if request.method == 'POST' and update_form.validate_on_submit():
        title = update_form.title.data
        content = update_form.content.data
        print(f"New Title: {title} | New Content: {content}")

        # Update will get added to the DB
        post.update(title=title,content=content)

        return redirect(url_for('post_detail', post_id = post_id))
    return render_template('post_update.html', update_form = update_form, post=post)

@app.route('/posts/delete/<post_id>', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        post.delete()
    return redirect(url_for('home'))

# Login Form Route
@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and logged_user.check_password(password):
            flash('Login successful')
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            flash('Login failed')
            return redirect(url_for('login'))

    return render_template('login.html',form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))