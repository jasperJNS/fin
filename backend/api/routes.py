from flask import Response, Flask, Blueprint

from backend.Fin import Fin
import backend.tests as bt

option_chain = Blueprint('/options', __name__)

@option_chain.route('/options/<ticker>', methods=['GET'])
def get_options(ticker):
    data = bt.get_fin(ticker)
    return Response(data, mimetype='application/json')
