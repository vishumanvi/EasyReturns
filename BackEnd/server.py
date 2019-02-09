from flask import Flask
from flask import request
from flask import jsonify
import redis
from ast import literal_eval
import usps_formats as uspsReq
import requests
import json

app = Flask(__name__)
_redis_port = 6379
redisList = ""
r = redis.StrictRedis(host='localhost', port=_redis_port, db=0)


def getDetails():
    # print(redisList)
    return literal_eval((r.get(redisList)).decode('utf-8'))


def setDetails(data):
    # print(redisList)
    r.set(redisList, data)


@app.route('/')
def index():
    return 'OK'


@app.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"


@app.route('/cost', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_calculate_cost():
    if request.method == 'POST':
        # get the fields from packageDetails
        # call the USPS apis to verify the address
        # call the USPS apis for cost calculation
        # Return different costs
        # req = {'zipSource': 95129,
        #        'zipDestination': 10001, 'ounces': 4.78}
        req = request.json
        xmlReq = uspsReq.getPriceCalculatorReq(req)
        url = (
            "http://production.shippingapis.com/ShippingAPI.dll?API=RateV4&XML={}".format(xmlReq))
        r = requests.get(url)
        response = r.content
        print(response)
        return ' ', 201


@app.route('/shipment', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_request_shipment(transactionDetails):
    if request.method == 'POST':
        # get entire package data like address etc from transactionDetails
        # call payment api to make payment
        # Once payment is done, store transaction details and address/package details in reddis
        # Generate a unique Id for this
        # return transactionId and uid
        pass


@app.route('/package/<uid>', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_get_package(uid):
    if request.method == 'GET':
        # get address details from reddis db for given uid
        # return details
        # this will  be used by postman/usps to get the details of package to deliver it
        pass


@app.route('/validate/<uid>', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_validate_package(uid):
    if request.method == 'GET':
        # validate if the package with given uid is valid or not
        # If the id exists in db along with transactionID
        # also check status to make sure that this is new package
        # This will be used by postman to validate a package
        # return true/false
        pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
