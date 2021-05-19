import numpy as np
import networkx as nx
from flask import Flask,  request,  jsonify


R = np.load(open("matrix_distance", "rb"))
G = nx.DiGraph(R)

def heuristic(a, b):
    return abs(a-b)

def findpassanddist(G, a, b):
    our_pass = nx.astar_path(G, a, b, heuristic)
    our_dist = nx.astar_path_length(G, a, b, heuristic)
    return our_pass, our_dist


app = Flask(__name__)

@app.route("/", methods=['POST'])
def upload():
    city_start = request.form.get('city_start')
    city_finish = request.form.get('city_finish')
    key = request.headers.get('X-API-KEY')
    if (key!='123321'):
        return jsonify(code = 401, body = 'Unauthorized')
    else:
        try:
            city_start = int(city_start)
            city_finish = int(city_finish)
            shortpass, dist = findpassanddist(G, city_start, city_finish)
            result =[ {
            'body': { 'path' : shortpass, 'distance' : dist}} ]
            return jsonify(result)
        except ValueError:
            return jsonify(code = 400, body= "Enter a number")
        except nx.NetworkXNoPath:
            return jsonify(code = 404, body = 'No road')
        except nx.NodeNotFound:
            return jsonify(code=400, body="Enter a number from 0 to 49")
        except TypeError:
            return jsonify(code=400, body="Enter a number")

if __name__ == "__main__":
    app.run()

