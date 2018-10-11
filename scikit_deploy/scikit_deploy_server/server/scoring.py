import pickle
import json
import pkg_resources
import numpy as np
import os
from flask import Blueprint, request, jsonify

model = pickle.loads(pkg_resources.resource_string(
    __name__, 'resources/clf.pkl'))
config = json.loads(pkg_resources.resource_string(
    __name__, 'resources/config.json'))

app_blueprint = Blueprint('app', __name__)


def _predict(sample):
    vec = np.array(sample).reshape(1, -1)
    res = model.predict(vec)
    return {a: b for a, b in zip(config["outputs"], res)}


ROUTE = f"{config.get('url_prefix', '')}/score"


@app_blueprint.route(ROUTE, methods=['GET'])
def score_endpoint():
    sample = []
    for v in config["inputs"]:
        p = request.args.get(v)
        if p is None:
            return f'Missing input in query string: {v}', 400
        try:
            sample.append(float(p))
        except ValueError:
            return f"Input could not be coerced to float: {v} = {p}"
    prediction = _predict(sample)
    return jsonify(dict(prediction=prediction))