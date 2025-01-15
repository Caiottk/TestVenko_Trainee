import requests
import pymysql
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    instance = os.environ.get('INSTANCE', 'Unknown')

    try:
        response = requests.post('http://monitor:5001/update_data')
        if response.status_code == 200:
            print('Nova coleta de dados acionada com sucesso.')
        else:
            print(f'Erro ao acionar coleta de dados: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao fazer requisição para o monitor: {e}')

    conn = pymysql.connect(host='db', user='root', password='root', database='monitoring')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM system_status ORDER BY timestamp DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()

    return render_template('index.html', instance=instance, data=data, db_name='monitoring')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
