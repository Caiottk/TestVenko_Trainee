from flask import Flask, render_template
import os
import pymysql

app = Flask(__name__)

@app.route('/')
def index():
    instance = os.environ.get('INSTANCE', 'Unknown')
    conn = pymysql.connect(host='db', user='root', password='root', database='monitoring')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM system_status ORDER BY timestamp DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()
    return render_template('index.html', instance=instance, data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
