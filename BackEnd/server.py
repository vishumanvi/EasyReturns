from flask import Flask
from flask import request, redirect, url_for
from flask import jsonify
import redis
from ast import literal_eval
import usps_formats as uspsReq
import requests
import json
import pickledb
import hashlib

app = Flask(__name__)
db_name = "shipments.db"
db = pickledb.load(db_name, True)


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


@app.route('/cost', methods=['POST'])
def api_calculate_cost():
    if request.method == 'POST':
        # get the fields from packageDetails
        # call the USPS apis to verify the address
        # call the USPS apis for cost calculation
        # Return different costs
        # req = {'zipSource': 95129,
        #        'zipDestination': 10001, 'ounces': 4.78}
        req = request.form
        xmlReq = uspsReq.getPriceCalculatorReq(req)
        url = (
            "http://production.shippingapis.com/ShippingAPI.dll?API=RateV4&XML={}".format(xmlReq))
        r = requests.get(url)
        res = uspsReq.getPriceResponse(r.content)
        result = json.dumps(res)
        # return json.dumps(res), 201
        return redirect("http://localhost:63342/USPS_EasyReturns/src/results.html?price1="+res[0]+"&price2="+res[1], code=200)
        # return redirect(url_for("http://localhost:63342/USPS_EasyReturns/src/results.html", messages=10), code=200)
        # return redirect(url_for("http://localhost:63342/USPS_EasyReturns/src/results.html", price1=100))

@app.route('/shipment', methods=['POST'])
def api_request_shipment():
    if request.method == 'POST':
        # get entire package data like address etc from transactionDetails
        # call payment api to make payment
        # Once payment is done, store transaction details and address/package details in reddis
        # Generate a unique Id for this
        # return transactionId and uid
        req = request.json
       # print (req)
        from_address = req['from_address1']
        to_address = req['to_address1']
        #category = req['category']
        category = "First Class"
        # date = req['date']
        date = "02/09/2019"
        # paymentID = req['payment-transaction']
        paymentID = "568425347"
        # payment_method = req['payment-method']
        payment_method = "Paypal"
        payment_amount = "49.55"

        hash_str = "{}:{}:{}:{}:{}".format(
            from_address, to_address, category, date, paymentID)
        hash_value = hashlib.sha1(hash_str.encode("UTF-8")).hexdigest()

        # print(hash_value)
        #shipment_details = dict()

        shipping_details = {'from-address': from_address, 'to-address': to_address, 'date': date,
                            'category': category, 'status': 'Created'}  # status: Created, AwaitingPickup, PickedUp, Delivered
        payment_details = {'payment-method': paymentID,
                           'payment-amount': payment_method, 'payment-transaction': payment_amount}
        #shipment_details[hash_value] = {'shipment-details': shipping_details, 'payment-details': payment_details}

        #print (shipment_details)
        db.set(hash_value, {'shipment-details': shipping_details,
                            'payment-details': payment_details})
        # print(db.get(hash_value))

        return hash_value, 201


@app.route('/package/<uid>', methods=['GET'])
def api_get_package(uid):
    if request.method == 'GET':
        # get address details from reddis db for given uid
        # return details
        # this will  be used by postman/usps to get the details of package to deliver it
        shipment = db.get(uid)
        if not shipment:
            return 'Not Found', 404
        shipment_details = shipment.get('shipment-details')
        # print(shipment_details)
        if shipment_details.get("status") == 'Created':
            res = {"originating-address": shipment_details.get("from-address"),
                   "destination-address": shipment_details.get("to-address"),
                   "category": shipment_details.get("category"),
                   "date": shipment_details.get("date")
                   }
            return json.dumps(res), 200
        return 'Invalid Request', 200


@app.route('/validate/<uid>', methods=['GET'])
def api_validate_package(uid):
    if request.method == 'GET':
        # validate if the package with given uid is valid or not
        # If the id exists in db along with transactionID
        # also check status to make sure that this is new package
        # This will be used by postman to validate a package
        shipment = db.get(uid)
        if not shipment:
            return 'Not Found', 404
        shipment_details = shipment.get('shipment-details')
        # print(shipment_details)
        if shipment_details.get("status") == 'Created':
            res = {"originating-address": shipment_details.get("from-address"),
                   "destination-address": shipment_details.get("to-address"),
                   "category": shipment_details.get("category"),
                   "date": shipment_details.get("date")
                   }
            return json.dumps(res), 200
        return 'Invalid Request', 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
