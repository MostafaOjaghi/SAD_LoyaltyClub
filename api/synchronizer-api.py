from http.server import BaseHTTPRequestHandler, HTTPServer


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        params = dict([tuple(s.split("=")) for s in post_data.decode("utf-8").split("&")])
        print("parameters : ", params)
        if self.path == "/customer":
            if fields_in_params(params, ["email", "customerID"]):
                self.send_response(200)
                self.end_headers()
                params["email"] = params["email"].replace("%40", "@")
                # can validate email here
                # call the method to save customer to DB
            else:
                self.send_error(400, "wrong parameters")

        elif self.path == "/product_order":
            if fields_in_params(params, ["product_orderID", "unit_price", "productID"]):
                self.send_response(200)
                self.end_headers()
                # validate params
                # save order to database
            else:
                self.send_error(400, "wrong parameters")

        elif self.path == "/customer_order":
            if fields_in_params(params, ["costumer_orderID", "costumerID", "product_orderID"]):
                self.send_response(200)
                self.end_headers()
                # validate params
                # save order to database
            else:
                self.send_error(400, "wrong parameters")
        return


def fields_in_params(params, fields):
    for field in fields:
        if field not in params:
            return False
    return True


print('starting server on port 8081...')
server_address = ('127.0.0.1', 8081)
httpd = HTTPServer(server_address, MyHandler)
httpd.serve_forever()
