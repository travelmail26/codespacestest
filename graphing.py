from flask import Flask, render_template, jsonify, request
import datetime

app = Flask(__name__)

# Initialize the data point
data_point = {'x': None, 'y': None}

@app.route('/', methods=['POST'])
def receive_data():
    global data_point
    # Get data from the local machine and store it
    data = request.get_json()
    print ('data recieved', data)
    data_point = {'x': data['timestamp'], 'y': data['random_number']}
    return 'Data received'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    global data_point
    # Send the data to the client
    response = jsonify(data_point)
    # Reset the data point
    data_point = {'x': None, 'y': None}
    return response

if __name__ == '__main__':
    app.run()
