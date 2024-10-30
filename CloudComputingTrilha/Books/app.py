from flask import Flask, render_template, request
import requests

app = Flask(__name__)

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

@app.route('/')
def index():
    return render_template('books.html')

@app.route('/search', methods=['POST'])
def search_books():
    query = request.form['query']
    
    params = {'q': query}
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    data = response.json()
    
    return render_template('books.html', books=data['items'])

if __name__ == '__main__':
    app.run(debug=True)
