from http.server import BaseHTTPRequestHandler, HTTPServer


class MyHandler(BaseHTTPRequestHandler):
    # initial db here
    # db = DBClass()
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        params = dict([tuple(s.split("=")) for s in post_data.decode("utf-8").split("&")])
        if self.path == "/customer":
            if MyHandler.fields_in_params(params, ["email", "customerID"]):
                self.send_response(200)
                self.end_headers()
                params["email"] = params["email"].replace("%40", "@")
                # call the method to save customer to DB
                # db.save_customer(params)
            else:
                self.send_error(400, "wrong parameters")

        elif self.path == "/product_order":
            if MyHandler.fields_in_params(params, ["product_orderID", "unit_price", "productID"]):
                self.send_response(200)
                self.end_headers()
                # save order to database
                # db.product_order(params)
            else:
                self.send_error(400, "wrong parameters")

        elif self.path == "/customer_order":
            if MyHandler.fields_in_params(params, ["costumer_orderID", "costumerID", "product_orderID"]):
                self.send_response(200)
                self.end_headers()
                # save order to database
                # db.customer_order(params)
            else:
                self.send_error(400, "wrong parameters")
        return

    def fields_in_params(params, fields):
        for field in fields:
            if field not in params:
                return False
        return True


class SynchronizerAPI:
    def __init__(self, server_address):
        self.server_address = server_address
        self.server = HTTPServer(server_address, MyHandler)

    def start_serving(self):
        print('starting server on {}:{}'.format(self.server_address[0], self.server_address[1]))
        self.server.serve_forever()


#s = SynchronizerAPI(('127.0.0.1', 8081))
#s.start_serving()



