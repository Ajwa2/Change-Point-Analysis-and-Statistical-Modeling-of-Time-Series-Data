from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Birhan Energies — Brent Price Analysis Dashboard (placeholder)"

if __name__ == '__main__':
    app.run(debug=True)
