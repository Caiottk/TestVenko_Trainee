from flask import Flask, render_template, request
import pymysql
import psutil
import socket
import subprocess
import time
import threading

app = Flask(__name__)

def get_system_info():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent
        ip = socket.gethostbyname(socket.gethostname())
        ping_latency = subprocess.getoutput("ping -c 1 8.8.8.8 | grep 'time=' | awk -F'time=' '{print $2}' | cut -d' ' -f1")
        if not ping_latency:
            ping_latency = 0.0
        return cpu_usage, mem_usage, ip, float(ping_latency)
    except Exception as e:
        print(f"Erro ao obter informações do sistema: {e}")
        return 0.0, 0.0, "N/A", 0.0

def insert_data(cpu_usage, mem_usage, ip, ping_latency):
    try:
        conn = pymysql.connect(host='db', user='root', password='root', database='monitoring')
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO system_status (cpu_usage, mem_usage, ip_address, ping_latency) VALUES (%s, %s, %s, %s)", 
                       (cpu_usage, mem_usage, ip, ping_latency))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao conectar ou inserir dados no banco de dados: {e}")

def periodic_data_collection():
    while True:
        cpu, mem, ip, ping = get_system_info()
        insert_data(cpu, mem, ip, ping)
        print(f"Dados coletados e inseridos automaticamente: {cpu}, {mem}, {ip}, {ping}")
        time.sleep(60)

@app.route('/update_data', methods=['POST'])
def update_data():
    cpu, mem, ip, ping = get_system_info()
    insert_data(cpu, mem, ip, ping)
    print(f"Dados coletados manualmente: {cpu}, {mem}, {ip}, {ping}")
    return 'Data collection triggered and saved successfully', 200

@app.route('/')
def index():
    try:
        conn = pymysql.connect(host='db', user='root', password='root', database='monitoring')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM system_status ORDER BY timestamp DESC LIMIT 1")
        data = cursor.fetchone()
        conn.close()
        
        if request.method == 'GET':
            update_data()

        return render_template('index.html', data=data)
    except Exception as e:
        print(f"Erro ao consultar o banco de dados: {e}")
        return render_template('index.html', data=None)

if __name__ == "__main__":
    threading.Thread(target=periodic_data_collection, daemon=True).start()
    app.run(host='0.0.0.0', port=5001)
