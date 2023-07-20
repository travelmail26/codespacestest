import plotly
import plotly.graph_objs as go
from flask import Flask, render_template, jsonify
import random
import datetime

app = Flask(__name__)

data = [go.Scatter(x=[], y=[], mode='lines', name='Real-time Data')]

layout = go.Layout(title='Real-time Graph')

fig = go.Figure(data=data, layout=layout)

@app.route('/')
def index():
    return render_template('index.html', plot=plotly.offline.plot(fig, output_type='div'))

print ('script run')

@app.route('/')
def get_data():
    # Generate some new data and return it as JSON
    x = datetime.datetime.now().isoformat()
    y = random.randint(1, 10)
    print ('this the value', y)
    return jsonify(x=x, y=y)

if __name__ == '__main__':
    app.run()