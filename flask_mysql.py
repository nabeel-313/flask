from flask import Flask, request, jsonify
import pymysql
app = Flask(__name__)

# book_list = [ {"id": 0, "author":"xyz", "language":"URDU","title":"Momin"},
#              {"id": 1, "author":"abc", "language":"ARABIC","title":"NABEEL"},
#              {"id": 2, "author":"lmn", "language":"ENGLISH","title":"AHMED"} ]
#GET = READ, POST = CREATE, PUT = UPDATE,  DELETE = DELETE

# conn = pymysql.connect(
#     host = 'localhost',
#     database = 'test',
#     user = 'root',
#     password = 'nabeel',
#     charset = 'utf8mb4',
#     cursorclass = pymysql.cursors.DictCursor
# )
# cursor = conn.cursor()
# sql_query = """CREATE TABLE IF NOT EXISTS book (
#              id integer PRIMARY KEY,
#              author text NOT NULL,
#              language text NOT NULL,
#              title text NOT NULL
# )"""
# cursor.execute(sql_query)

    
def db_connection():
    conn = None
    try:
        conn = pymysql.connect(host = 'localhost',
                                database = 'test',
                                user = 'root',
                                password = 'nabeel',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor
                                )
    except pymysql.error as e:
        print(e)
    return conn
        
@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == "GET":
        cursor = cursor.execute("SELECT * FROM book")
        books = [
            dict(id=row['id'], author=row['author'], language=row['language'], title=row['title'])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if  request.method == "POST":
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        
        sql = """ INSERT INTO book (author, language, title) VALUES (%s,%s,%s)"""
        cursor = cursor.execute(sql, (new_author, new_lang, new_title))
        conn.commit()
        return f"Book with id : {cursor.lastrowid} created successfully"
    
@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == 'GET':
        cursor.execute('SELECT * FROM book WHERE id =?', (id, ))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book)
        else:
            return "Some thing went wrong "
    
    if request.method == 'PUT':
        sql = """ UPDATE book SET title = ?, author = ?, language = ? where id = ? """
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        updated_book = {
                    'id' : id,
                    'author' : author,
                    'language' : language,
                    'title' : title
                }
        conn.execute(sql, (author, language, title, id))
        conn.commit()
        return jsonify(updated_book)
    
    if request.method == 'DELETE':
        sql = """ DELETE FROM book WHERE id=? """
        conn.execute(sql, (id, ))
        conn.commit()
        return "The book  with id : {} has been deleted ".format(id)
            
        
    
                    
if __name__ == '__main__':
    app.run(debug=True)
    
    
    