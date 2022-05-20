from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from forms import Base, Book

app = Flask(__name__)

engine = create_engine('sqlite:///home_library.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/', methods=['GET', 'POST'])
@app.route('/books/', methods=['GET', 'POST'])
def showBooks():
    books = session.query(Book).all()
    return render_template("books.html", books=books)


@app.route('/books/new/', methods=['GET', 'POST'])
def newBook():
    if request.method == 'POST':
        newBook = Book(title=request.form['name'], author=request.form['author'], genre=request.form['genre'])
        session.add(newBook)
        session.commit()
        return redirect(url_for('showBooks'))
    else:
        return render_template('newBook.html')



@app.route("/books/<int:book_id>/", methods=['GET', 'POST'])
def editBook(book_id):
    editedBook = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedBook.title = request.form['name']
            return redirect(url_for('showBooks'))
    else:
        return render_template('editBook.html', book=editedBook)


@app.route('/books/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    bookToDelete = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(bookToDelete)
        session.commit()
        return redirect(url_for('showBooks', book_id=book_id))
    else:
        return render_template('deleteBook.html', book=bookToDelete)


if __name__ == "__main__":
    app.run(debug=True)