from flask import Blueprint, request, render_template, redirect, url_for, flash
from book_app.models import BookGenre, WishToRead, ReadCompleted, User
from book_app.forms import BookForm, LoginForm, SignUpForm

from book_app.extensions import app, db, bcrypt

from flask_login import login_required, login_user, logout_user, current_user

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

@main.route('/')
def homepage():
    return render_template('home.html')

@main.route('/bookwishlist')
def bookwishlist():
    all_wishlists = WishToRead.query.all()
    return render_template('bookwishlist.html', all_wishlists=all_wishlists)

@main.route('/new_bookwishlist', methods=['GET', 'POST'])
def new_bookwishlist():
    form = BookForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            book_title = request.form.get('title')
            book_description = request.form.get('description')
            photo_url = request.form.get('photo_url')
            genre = request.form.get('category')
            created_by = current_user
            new_book = WishToRead(book_name=book_title, description=book_description, category=genre, photo_url=photo_url, created_by=created_by)

            current_user.wishtoreads.append(new_book)
            db.session.add(new_book)

            db.session.commit()

            flash('Successfully Added!')
            return redirect(url_for('main.bookwishlist', book_id=new_book.id))
    return render_template('new_bookwishlist.html', form=form)

@main.route('/new_bookwishlist/<wishlist_id>', methods=['GET', 'POST'])
def wishlistbook_detail(wishlist_id):
    book = WishToRead.query.get(wishlist_id)
    form = BookForm(obj=book)

    if request.method == 'POST':
        if form.validate_on_submit():
            book.book_name = form.title.data
            book.description = form.description.data
            book.photo_url = form.photo_url.data
            book.category = form.category.data

            db.session.add(book)
            db.session.commit()

            flash('Successfully Updated!')
            return redirect(url_for('main.bookwishlist', book_id=book.id))

    return render_template('bookwishlist_detail.html', book=book, form=form)

@main.route('/bookcompleted')
def bookcompleted():
    all_completes = ReadCompleted.query.all()
    return render_template('bookcompleted.html', all_completes=all_completes)

@main.route('/new_bookcompleted', methods=['GET', 'POST'])
def new_bookcompleted():
    form = BookForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            book_title = request.form.get('title')
            book_description = request.form.get('description')
            photo_url = request.form.get('photo_url')
            genre = request.form.get('category')
            created_by = current_user
            new_book = ReadCompleted(book_name=book_title, description=book_description, category=genre, photo_url=photo_url, created_by=created_by)

            current_user.readcompletes.append(new_book)
            
            db.session.add(new_book)
            db.session.commit()

            flash('Successfully Added!')
            return redirect(url_for('main.bookcompleted', book_id=new_book.id))
    return render_template('new_bookcompleted.html', form=form)

@main.route('/new_bookcompleted/<complete_id>', methods=['GET', 'POST'])
def completedbook_detail(complete_id):
    book = ReadCompleted.query.get(complete_id)
    form = BookForm(obj=book)

    if request.method == 'POST':
        if form.validate_on_submit():
            book.book_name = form.title.data
            book.description = form.description.data
            book.photo_url = form.photo_url.data
            book.category = form.category.data

            db.session.add(book)
            db.session.commit()

            flash('Successfully Updated!')
            return redirect(url_for('main.bookcompleted', book_id=book.id))

    return render_template('completedbook_detail.html', book=book, form=form)

# Auth route
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.data['password']).decode('utf-8')
            user = User(
                username=form.username.data,
                password=hashed_password
            )
            db.session.add(user)
            db.session.commit()
            flash('Account Created.')
            print('created')
            return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))