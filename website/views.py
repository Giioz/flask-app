from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        title = request.form.get('title')

        if not text:
            flash('Post cannot be empty', category='error')
        elif not title:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, title=title, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='succes')
            return redirect(url_for("views.home"))
    return render_template('create_post.html', user=current_user)