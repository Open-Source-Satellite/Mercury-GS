import sys
from flask import Flask
from flask_restful import Api
from api.resources.telemetry import Telemetry

app = Flask(__name__)
api = Api(app)

telemetry = Telemetry()

api.add_resource(Telemetry, '/telemetry', resource_class_kwargs={
    'tlm_channel': 1,
    'tc_timeout': 100,
    'is_continuous': False
})

if __name__ == '__main__':
    app.run(debug=True)



