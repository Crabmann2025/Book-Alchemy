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

# Hilfsfunktion zum sicheren Parsen von Datum
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Add a new author to the database.
    Converts string dates (YYYY-MM-DD) from the form to Python date objects.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date_str = request.form.get('birthdate')
        date_of_death_str = request.form.get('date_of_death')

        # Strings zu datetime.date konvertieren
        birth_date = parse_date(birth_date_str)
        date_of_death = parse_date(date_of_death_str)

        # Author-Objekt erstellen
        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        db.session.add(new_author)
        db.session.commit()
        flash(f'Author "{name}" added successfully!')
        return redirect(url_for('add_author'))

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Add a new book to the database.
    Author must be selected from existing authors.
    """
    authors = Author.query.all()  # get all authors for the dropdown

    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year_str = request.form.get('publication_year')
        author_id_str = request.form.get('author_id')

        # Convert publication_year to int if provided
        publication_year = int(publication_year_str) if publication_year_str else None
        author_id = int(author_id_str) if author_id_str else None

        # Book-Objekt erstellen
        new_book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=author_id
        )

        db.session.add(new_book)
        db.session.commit()
        flash(f'Book "{title}" added successfully!')
        return redirect(url_for('add_book'))

    return render_template('add_book.html', authors=authors)


@app.route('/')
def home():
    """
    Zeigt alle Bücher auf der Startseite an.
    Wenn ein Suchbegriff vorhanden ist, werden nur passende Bücher angezeigt.
    """
    search_query = request.args.get('search')  # holt den Suchtext aus dem Formular
    if search_query:
        # Suche in Titel und Autorname
        books = Book.query.join(Author).filter(
            (Book.title.ilike(f"%{search_query}%")) |
            (Author.name.ilike(f"%{search_query}%"))
        ).all()
        if not books:
            flash(f'Keine Bücher gefunden für "{search_query}"')
    else:
        books = Book.query.all()
    return render_template('home.html', books=books)


if __name__ == "__main__":
    app.run(debug=True)