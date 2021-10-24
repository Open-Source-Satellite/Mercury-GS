import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/v1/ping', methods=['GET'])
def api_all():
    return jsonify({
        'pong': 'success',
    })


@app.route('/api/v1/telecommand/send/request', methods=['POST'])
def send_telecommand_request():
    # TODO: need to add data validation here.
    # TODO: How does middleware flask work? Need to add Auth JWT M2M token validation.
    body = request.json
    telecommand_number = body['telecommand_number']
    telecommand_data = body['telecommand_data']
    telecommand_data_type = body['telecommand_data_type']
    is_continuous = body['is_continuous']

    print('TC: {}'.format(telecommand_number))
    print('Data: {}'.format(telecommand_data))
    print('DataType: {}'.format(telecommand_data_type))
    print('Is continuous: {}'.format(is_continuous))

    # TODO: Talk to Jamie about connecting this to the right functions.

    return 'OK'

@app.route('/api/v1/telemetry/send/request', methods=['POST'])
def send_telemetry_request():
    body = request.json
    tlm_channel =  body['tlm_channel']
    is_continuous =  body['is_continuous'] 

    print('Channel: {}'.format(tlm_channel))
    print('Is continuous: {}'.format(is_continuous))

    # TODO: Talk to Jamie about connecting this to the right functions.

    return 'OK'

@app.route('/api/v1/transmit/test', methods=['POST'])
def transmit_test():
    return 'OK'

app.run()