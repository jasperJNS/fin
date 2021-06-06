from flask import Response, Flask, Blueprint, make_response
from flask_cors import cross_origin, CORS

import logging

from backend.Fin import Fin
import backend.tests as bt

option_chain = Blueprint('/options', __name__)



@option_chain.route('/options/<ticker>', methods=['POST', 'OPTIONS'])
@cross_origin()
def get_options(ticker):
    data = bt.get_fin(ticker)
    #headers={'Access-Control-Allow-Origin': '*'}
    response = Response(data, mimetype='application/json')
    return response

@option_chain.route('/options/', methods=['POST'])
def testing():
    x = 'hello'
    print(x)
    response = Response(x, mimetype='application/json')
    return response

