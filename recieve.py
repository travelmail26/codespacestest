from flask import Flask, request
import datetime
import time

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    timestamp = datetime.datetime.now().isoformat()
    print(f'Received data: {data}, {timestamp}')
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
