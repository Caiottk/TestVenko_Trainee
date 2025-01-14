import pymysql
import time
import psutil
import socket
import subprocess

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

def insert_data():
    try:
        conn = pymysql.connect(host='db', user='root', password='root', database='monitoring')
        cursor = conn.cursor()
        
        while True:
            cpu, mem, ip, ping = get_system_info()
            cursor.execute("INSERT INTO system_status (cpu_usage, mem_usage, ip_address, ping_latency) VALUES (%s, %s, %s, %s)", (cpu, mem, ip, ping))
            conn.commit()
            time.sleep(60)
    except Exception as e:
        print(f"Erro ao conectar ou inserir dados no banco de dados: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    insert_data()
