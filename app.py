from flask import Flask, request, render_template, redirect, url_for, flash
from extensions import db
from data_models import Author, Book
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database configuration (SQLite)
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Funktion zum Parsen von Datum-Strings
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

# add author
@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date = parse_date(request.form.get('birthdate'))
        date_of_death = parse_date(request.form.get('date_of_death'))

        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()
        flash(f'Author "{name}" added successfully!')
        return redirect(url_for('add_author'))

    return render_template('add_author.html')

# add book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = Author.query.all()  # get all authors for the dropdown

    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year = int(request.form.get('publication_year')) if request.form.get('publication_year') else None
        author_id = int(request.form.get('author_id')) if request.form.get('author_id') else None

        new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        flash(f'Book "{title}" added successfully!')
        return redirect(url_for('add_book'))

    return render_template('add_book.html', authors=authors)


@app.route('/')
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)


# Delete
@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = book.author
    db.session.delete(book)
    db.session.commit()

    # Prüfen, ob der Autor noch andere Bücher hat
    if not author.books:
        db.session.delete(author)
        db.session.commit()
        flash(f'Book "{book.title}" and its author "{author.name}" were deleted!')
    else:
        flash(f'Book "{book.title}" was deleted!')

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
