from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Feedback, User
from forms import RegisterUserForm, LoginUserForm, FeedbackForm
# from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Register user and add to the db and session"""
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        
        session['username'] = new_user.username
        db.session.add(new_user)
        db.session.commit()
        return redirect(f'/users/{new_user.username}')
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Login user, if authenticated add username to session. """
    form = LoginUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')




@app.route('/users/<username>')
def show_user_info(username):
    """Check if user is logged in and if it the correct user accessing the page, show details"""
    if 'username' not in session:
        flash("Log in before accessing this page", "error")
        return redirect('/login')
    user = User.query.get_or_404(username)
    feedback = Feedback.query.filter(Feedback.username == username).all()
    if session['username'] != user.username:
        flash("You do not have access to this user", "error")
        return redirect('/login')
    return render_template('user_info.html', user=user, feedback=feedback)



@app.route('/feedback/<int:id>/update', methods=["GET", "POST"])
def update_feedback(id):
    """If user is loged in and is the correct user, update feedback"""
    if 'username' not in session:
        flash("Log in before accessing this page", "error")
        return redirect('/login')
    feedback = Feedback.query.get_or_404(id)
    form = FeedbackForm(obj=feedback)

    if session['username'] != feedback.username:
        flash("You dont have access to this page", "error")
        return redirect('/login')
    else:      
      
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(f'/users/{feedback.username}')

    return render_template("update_feedback.html",form=form)



@app.route('/feedback/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    """If user is logged in and is the correct user, add feedback"""
    if 'username' not in session:
        flash("Log in before accessing this page", "error")
        return redirect('/login')

    if session['username'] != username:
        flash("You dont have access to this page", "error")
        return redirect('/login')

    user = User.query.get_or_404(username)
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=user.username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')

    return render_template('add_feedback.html', user=user, form=form)


@app.route('/feedback/<int:id>/delete', methods=["GET", "POST"])
def delete_feedback_instance(id):
    """If user is logged in and is the correct user delete the requested feedback"""
    if 'username' not in session:
        flash("Log in before accessing this page", "error")
        return redirect('/login')
    
    feedback = Feedback.query.get_or_404(id)

    if session['username'] != feedback.username:
        flash("You dont have access to this page", "error")
        return redirect('/login')
    
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f"/users/{feedback.username}")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_account(username):
    """If user is logged in and is the correct user delete the requested user account"""
    if 'username' not in session:
        flash("Log in before accessing this page", "error")
        return redirect('/login')

    if session['username'] != username:
        flash("You dont have access to this page", "error")
        return redirect('/login')
    
    user = User.query.get_or_404(username)
    feedback = Feedback.query.filter(Feedback.username == username).all()
    db.session.delete(user)
    for feed in feedback:
        db.session.delete(feed)
        db.session.commit()
    session.pop("username")
    return redirect('/')