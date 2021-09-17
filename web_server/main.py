import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/v1/ping', methods=['GET'])
def api_all():
    return jsonify({
        'pong': 'success',
    })

app.run()