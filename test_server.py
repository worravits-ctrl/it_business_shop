from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>IT Business Shop</h1>
    <p>Server is working on port 8000!</p>
    <a href="/test">Test Page</a>
    '''

@app.route('/test')
def test():
    return '''
    <h1>Test Successful!</h1>
    <p>Flask app is running properly.</p>
    <a href="/">Back to Home</a>
    '''

if __name__ == '__main__':
    print("Starting IT Business Shop on http://127.0.0.1:8000")
    app.run(host='127.0.0.1', port=8000, debug=True)