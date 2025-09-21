from flask import Flask, request, render_template, redirect, url_for, flash
from extensions import db
from data_models import Author, Book
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database configuration (SQLite)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

def parse_date(date_str):
    """
    Convert a string in "YYYY-MM-DD" format to a Python date object.
    Returns None if the input is invalid or empty.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Home page route.
    Displays all books in the library or filters by a search query if provided.
    """
    search_query = request.form.get('search') if request.method == 'POST' else None

    if search_query:
        books = Book.query.filter(Book.title.ilike(f"%{search_query}%")).all()
        if not books:
            flash(f'No books found containing "{search_query}".')
    else:
        books = Book.query.all()

    return render_template('home.html', books=books)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Route to add a new author.
    GET: Display the form to add an author.
    POST: Add the author to the database after parsing dates.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date = parse_date(request.form.get('birthdate'))
        date_of_death = parse_date(request.form.get('date_of_death'))

        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        db.session.add(new_author)
        db.session.commit()
        flash(f'Author "{name}" successfully added!')
        return redirect(url_for('add_author'))

    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Route to add a new book.
    GET: Display the form to add a book with a dropdown of authors.
    POST: Add the book to the database.
    """
    authors = Author.query.all()

    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year = int(request.form.get('publication_year')) if request.form.get('publication_year') else None
        author_id = int(request.form.get('author_id')) if request.form.get('author_id') else None

        new_book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=author_id
        )

        db.session.add(new_book)
        db.session.commit()
        flash(f'Book "{title}" successfully added!')
        return redirect(url_for('add_book'))

    return render_template('add_book.html', authors=authors)

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Delete a specific book by ID.
    Also deletes the author if they have no other books.
    """
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    db.session.commit()

    if not author.books:
        db.session.delete(author)
        db.session.commit()

    flash(f'Book "{book.title}" successfully deleted!')
    return redirect(url_for('home'))

@app.route('/author/<int:author_id>/delete', methods=['POST'])
def delete_author(author_id):
    """
    Delete a specific author by ID.
    Also deletes all books associated with that author.
    """
    author = Author.query.get_or_404(author_id)
    for book in author.books:
        db.session.delete(book)
    db.session.delete(author)
    db.session.commit()
    flash(f'Author "{author.name}" and all their books were deleted!')
    return redirect(url_for('home'))

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """
    Detail page for a specific book.
    Displays all information about the book and its author.
    """
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

@app.route('/author/<int:author_id>')
def author_detail(author_id):
    """
    Detail page for a specific author.
    Displays author info and all books by the author.
    """
    author = Author.query.get_or_404(author_id)
    return render_template('author_detail.html', author=author)

if __name__ == "__main__":
    app.run(debug=True)
