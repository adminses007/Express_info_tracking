from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    tracking_number = request.form['tracking_number']
    conn = sqlite3.connect('express_info.db')
    cursor = conn.cursor()
    cursor.execute("SELECT tracking_number, status FROM express WHERE tracking_number = ?", (tracking_number,))
    express_info = cursor.fetchone()
    conn.close()
    if express_info:
        return render_template('search.html', tracking_number=express_info[0], status=express_info[1])
    else:
        return render_template('not_found.html')

if __name__ == '__main__':
    app.run(host='192.168.1.103', port=5000, debug=True)


