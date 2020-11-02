"""
    Small Web application to Geocode Irish addresses
"""
from flask import Flask, abort, jsonify, request
from validator import validate_address
from geocoder import geocoder


def create_app():

    app = Flask(__name__)

    @app.errorhandler(400)
    def bad_address(e):
        return jsonify(error="Invalid Address"), 400

    @app.errorhandler(404)
    def address_not_found(e):
        return jsonify(error="Address not found"), 404
    
    @app.route("/geocode")
    def geocode():
        """
            Call the Geocoder with a given address
        """
        address_string = request.args.get('address')
        if validate_address(address_string):
            # TODO similar to the CLI, there is too much of the 
            # Geocoder's internal API being used here
            # Refactor so that geocode is called on instantiation
            address_match = geocoder.Address(address_string)
            try:
                address_match.geocode()
                return jsonify(coordinates=address_match.coords)                  
            except geocoder.AddressNotMatched:
                abort(404, address_not_found)

        else:
            abort(400, description="Invalid Address")

    return app
