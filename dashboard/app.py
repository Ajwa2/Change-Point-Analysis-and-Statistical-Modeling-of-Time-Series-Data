from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import json
import os

app = Flask(__name__, static_folder='frontend/dist')
CORS(app)

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_ROOT = os.path.normpath(os.path.join(ROOT, '..', 'data'))


@app.route('/')
def index():
    # serve the frontend
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/prices')
def api_prices():
    # Return historical prices as JSON
    csv_path = os.path.join(DATA_ROOT, 'BrentOilPrices.csv')
    df = pd.read_csv(csv_path, parse_dates=[0], dayfirst=True)
    df.columns = ['date', 'price']
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    records = df.to_dict(orient='records')
    return jsonify(records)


@app.route('/api/events')
def api_events():
    events_path = os.path.join(DATA_ROOT, 'processed', 'events.csv')
    df = pd.read_csv(events_path, parse_dates=['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    return jsonify(df.to_dict(orient='records'))


@app.route('/api/change_points')
def api_change_points():
    cp_path = os.path.join(DATA_ROOT, 'processed', 'change_points.json')
    if os.path.exists(cp_path):
        with open(cp_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
