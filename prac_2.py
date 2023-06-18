from flask import Flask, request, jsonify

app = Flask(__name__)

book_list = [ {"id": 0, "author":"xyz", "language":"URDU","title":"Momin"},
             {"id": 1, "author":"abc", "language":"ARABIC","title":"NABEEL"},
             {"id": 2, "author":"lmn", "language":"ENGLISH","title":"AHMED"}
    
]

#GET = READ, POST = CREATE, PUT = UPDATE,  DELETE = DELETE
@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == "GET":
        if len(book_list)>0:
            return jsonify(book_list)
        else:
            "No books found"    
    if  request.method == "POST":
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        iD = book_list[-1]['id']+1
        
        new_object = {
            'id': iD,
            'author': new_author,
            'language': new_lang,
            'title': new_title      
        }
        book_list.append(new_object)
        return jsonify(book_list)
    
@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    if request.method == 'GET':
        for book in book_list:
            if book['id'] == id:
                return jsonify(book)
            pass
    
    if request.method == 'PUT':
        for book in book_list:
            if book['id'] == id:
                book['author'] = request.form['author']
                book['language'] = request.form['language']
                book['title'] = request.form['title']
                updated_book = {
                    'id' : id,
                    'author' : book['author'],
                    'language' : book['language'],
                    'title' : book['title']
                }
                return jsonify(updated_book)
    
    if request.method == 'DELETE':
        for index, book in enumerate(book_list):
            if book['id'] == id:
                book_list.pop(index)
                return jsonify(book_list)
            
        
    
                    
if __name__ == '__main__':
    app.run(debug=True)
    
    
    