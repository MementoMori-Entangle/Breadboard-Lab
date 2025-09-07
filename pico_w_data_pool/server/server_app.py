import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# PostgreSQL接続情報
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'BME280')
DB_USER = os.getenv('DB_USER', 'BME280')
DB_PASS = os.getenv('DB_PASS', 's#gs1Gk3Dh8sa!g3s')

# BME280データ用テーブル作成（初回のみ）
def init_db():
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bme280_data (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            humidity REAL,
            pressure REAL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json(force=True)
        # データがリストの場合は複数件、dictなら1件
        if isinstance(data, list):
            for entry in data:
                save_bme280(entry)
        elif isinstance(data, dict):
            save_bme280(data)
        return 'OK', 200
    except Exception as e:
        print('Error:', e)
        return 'Error', 500

@app.route('/api/data/fetch', methods=['POST'])
def fetch_request():
    # Pico側からデータ取得要求が来た場合の処理
    req_json = request.get_json(force=True)
    index = req_json.get('index')
    print(f"データ取得要求: index={index}")
    # index値を付与して返す
    return jsonify({'status': 'done', 'index': index}), 200

@app.route('/api/data/fetch_status', methods=['GET'])
def fetch_status():
    # Pico側から取得完了確認
    return jsonify({'status': 'done'}), 200

@app.route('/api/data/warn', methods=['POST'])
def warn():
    data = request.get_json(force=True)
    print('Pool warning:', data)
    return 'Warn received', 200

def save_bme280(entry):
    # entry: {"temperature": float, "humidity": float, "pressure": float}
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO bme280_data (temperature, humidity, pressure)
            VALUES (%s, %s, %s)
        ''', (entry.get('temperature'), entry.get('humidity'), entry.get('pressure')))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print('DB insert error:', e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
