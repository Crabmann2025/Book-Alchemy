# Digital Library Flask App 📚

A simple digital library web application built with Flask, SQLite, and SQLAlchemy.
Manage authors and books, search, view details, and delete records, all with a modern, user-friendly interface.

## Features ✨
  - Add, view, and delete authors and books.
  - Each book links to its author, and each author page lists all their books.
  - Keyword search for books by title.
  - Detail pages for books and authors.
  - Modern UI with responsive design.
  - Prepare for UI redesign, book ratings, and AI book suggestions.
  - Fully functional home page showing all books.
  - Delete books or authors, with cascading deletion of related records.

## Screenshots 🖼️
  - Home page: Lists all books with author and links to detail pages.
  - Add Author / Add Book pages: Forms for creating records.
  - Book / Author Detail pages: View all relevant information in a clean layout.

## Installation 🛠️

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/digital-library.git
    cd digital-library


2. Create a virtual environment:
     ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows


3. Install dependencies:
     ```bash
    pip install -r requirements.txt


  - requirements.txt should contain:
    ```bash
    Flask
    Flask-SQLAlchemy


4. Run the application:
    ```bash
    python app.py


5. Open your browser at:
    ```bash
    http://127.0.0.1:5000/


## Usage 📖
- Home Page
  - Displays all books with author names.
  - Buttons to Add Author, Add Book, and Search.
  - Click on book or author titles to view details.
  - Delete books or authors from the home page or detail pages.

- Add Author
  - Go to /add_author.
  - Fill in name, birth date, and optionally date of death.
  - Submit to add the author to the library.

- Add Book
  - Go to /add_book.
  - Fill in title, ISBN, publication year, and select an author.
  - Submit to add the book.

- Detail Pages
  - Book details: /book/<book_id>
  - Author details: /author/<author_id>
  - Includes back buttons to home and add forms.

- Search Books
  - Enter a keyword in the search field on the home page.
  - Results show books with titles containing the keyword.
  - Message shown if no books match.

- Delete Records
  - Books: /book/<book_id>/delete (POST)
  - Authors: /author/<author_id>/delete (POST, deletes all related books)
