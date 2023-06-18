from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello Maryam"

#for dynamic routing
@app.route("/<name>")
def dynamic_route(name):
    return 'Welcome , {}'.format(name)



#while development make debug True
if __name__ == '__main__':
    app.run(debug=True)