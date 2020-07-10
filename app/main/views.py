from . import main
from flask import render_template,flash,request,redirect,url_for,abort
from flask_login import login_required,current_user
from ..models import User,Post,Comment
from .forms import UpdateProfile,PostForm,CommentForm
from .. import db,photos
from ..request import get_quotes
from ..email import mail_message

# Views

@main.route('/')
def index():
    """
    view index page and its data
    """
    title = 'My Blog'
    #fetch quotes
    quotes = get_quotes()
    print(quotes)
    return render_template('index.html', title = title, quotes = quotes )

@main.route('/post/new',methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    
    if form.validate_on_submit():
        #user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        post = Post(title = form.title.data, content = form.content.data, user = current_user)
        db.session.add(post)
        db.session.commit()
        #mail_message("New Post Alert!","email/alert_user",user.email,user=user)
        flash('Your post has been created!', 'success')
        return redirect(url_for('.home'))
    title = 'New Post' 
    return render_template('posts.html',title = title,form = form)

@main.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('that_post.html', post = post )

@main.route('/home/comment/<int:post_id>',methods = ['GET','POST'])
@login_required
def comment(post_id):
    '''
    View root page function that returns the comments and its data
    '''
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        comment = form.comment.data
        #date_posted = form.date_posted.data
        comment = Comment(comment = comment,user_id = current_user._get_current_object().id,post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!')
        return redirect(url_for('.comment',post_id=post_id))
    
    all_comments = Comment.query.order_by(Comment.date_posted.desc()).all()
    return render_template("comments.html",form=form, comment = all_comments,post = post)

@main.route('/post/<int:post_id>/update',methods = ['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
       post.title = form.title.data  
       post.content = form.content.data
       db.session.commit()
       flash('Your post has been updated!')
       return redirect(url_for('.home', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    title = 'Update Post'
    return render_template('posts.html',title = title,form = form)



@main.route('/home', methods = ['GET','POST'])
def home():
    '''
    View root page function that returns the home page and its data
    '''
    #quotes = get_quotes()
    #page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    title = 'Home - Welcome to My BLog'
    return render_template('home.html', title = title, posts = posts)

@main.route('/user/post/<string:username>')
def user_post(username):
    '''
    View root page function that returns the user_post page and its data
    '''
    #page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user=user).order_by(Post.date_posted.desc()).all()
    title = 'Home - Welcome to My BLog'
    return render_template('user_post.html', user=user,title = title, posts = posts)

@main.route('/home/comment/<int:comment_id>')
def solo_comment(comment_id):
    '''
    View root page function that returns the solo_comment page and its data
    '''
    #page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    comments = Comment.query.filter_by(user=user).order_by(Comment.date_posted.desc(comment_id)).all()
    title = 'Home - Welcome to My BLog'
    return render_template('solo_comment.html', user=user,title = title, comments = comments)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/post/<int:post_id>/delete',methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!')
    return redirect(url_for('.home'))

@main.route('/home/comment/<int:post_id>/delete',methods = ['POST'])
@login_required
def delete_comment(post_id):
    post = Post.query.get_or_404(post_id)  
    comment = Comment.query.filter_by(post_id = post.id).first()
    try:
        db.session.delete(comment)
        db.session.commit()
    except:
        'UnmappedInstanceError'
    
    flash('Your comment has been deleted!')
    return redirect(url_for('.comment',post_id=post_id))


@main.route('/home/subscribe')
@login_required
def subscribe():
    if post.user != current_user:
        abort(403)
    
