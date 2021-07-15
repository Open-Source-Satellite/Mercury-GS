import sys
from flask import Flask
from flask_restful import Api
from api.resources.telemetry import Telemetry
# from myapi.resources.bar import Bar
# from myapi.resources.baz import Baz

# from flask import Flask
# from flask_restful import Resource, Api
# from telemetry import tlm_request_send

app = Flask(__name__)
api = Api(app)

api.add_resource(Telemetry, '/telemetry/<int:tlm_channel>/', )
class HelloWorld(Resource):
    def get(self):
        tlm_request_send(1, False);
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)



