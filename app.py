import json
import urllib3

from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    """This method handles the http requests for the API.AI webhook

    This is meant to be used in conjunction with the translate API.AI agent
    """

    # Get request parameters
    req = request.get_json(silent=True, force=True)
    action = req.get('result').get('action')

    if action == 'get_line_status':

        try:
            line = req['result']['parameters'].get('line')
            disruptions = get_status(line)
            if len(disruptions):
                output = line + " is disrupted"
            else:
                output = line + " has no disruptions"
        except Exception as ex:
            output = str(ex)


        # Compose the response to API.AI
        res = {'speech': output,
               'displayText': output,
               # 'contextOut': req['result']['contexts']
               }

    return make_response(jsonify(res))

def get_status(line):
    request = urllib3.PoolManager()
    url = "https://api.tfl.gov.uk/Line/{}/Disruption/".format(line) #'?api_id={}&app_key={}".format(line, "fe639503", "d99f264b6f65f3ff5920c8b4576d138c")
    response = request.request('GET', url)
    data = response.data.decode('UTF-8')
    return json.loads(data)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
