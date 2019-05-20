import json
import random

import flask
import flask_restful

# Configuration of the server
config = {'ip': '0.0.0.0', 'port': 80}

# noinspection PyTypeChecker
app = flask.Flask(__name__, static_url_path="/static")


@app.route('/')
@app.route('/home')
def home():
    """
    Simple rendering of the `index.html` page.

    Returns:
        Flask template return.
    """

    template_return = flask.render_template('index.html')

    return template_return


class APIGenerator(flask_restful.Resource):
    """
    Simple class from `flask_restful.Resource` to handle API endpoint
    """

    @staticmethod
    def get(bus: str):
        """
        HTTP GET request for random bus time of arrival.

        Args:
            bus: Bus to retrieve information of.

        Returns:
            json data filled if bus found.
        """

        buses = ['L2', 'X4', 'S1', 'A6', 'M3', 'R5']
        api_data = {"data": 0}

        if bus.capitalize() in buses:
            api_data['data'] = 'Found 1 bus'
            api_data['bus_name'] = bus
            arrival_time = random.choice([minutes for minutes in range(1, 6)])
            api_data['arrival'] = f'{arrival_time} mins'
            code = 200
            api_data['code'] = code

        else:
            api_data['data'] = 'Bus not found'
            code = 201
            api_data['code'] = code

        return flask.Response(json.dumps(api_data), status=code, mimetype='application/json')


# API Endpoint for random bus data
API = flask_restful.Api(app)
API.add_resource(APIGenerator, '/api/<string:bus>')


if __name__ == "__main__":
    app.run(host=config['ip'], port=config['port'], threaded=True, debug=True)
