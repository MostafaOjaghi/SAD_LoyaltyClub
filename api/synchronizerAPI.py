from http.server import BaseHTTPRequestHandler, HTTPServer
from db.DB import DBClass


class MyHandler(BaseHTTPRequestHandler):
    # initial db here
    # db = DBClass()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        params = dict([tuple(s.split("=")) for s in post_data.decode("utf-8").split("&")])
        if self.path == "/customer":
            if MyHandler.fields_in_params(params, ["email", "customerID", "birthday"]):
                self.send_response(200)
                self.end_headers()
                params["email"] = params["email"].replace("%40", "@")
                # call the method to save customer to DB
                self.db.insert_customer(params)
            else:
                self.send_error(400, "wrong parameters")

        elif self.path == "/order":
            if MyHandler.fields_in_params(params, ["orderID", "customerID", "date", "total_price", "discount_price", "birthday_discount_price"]):
                self.send_response(200)
                self.end_headers()
                # save order to database
                self.db.insert_order(params)
            else:
                self.send_error(400, "wrong parameters")
        return

    @staticmethod
    def fields_in_params(params, fields):
        for field in fields:
            if field not in params:
                return False
        return True


class SynchronizerAPI:
    def __init__(self, server_address, DB):
        MyHandler.db = DB
        self.server_address = server_address
        self.server = HTTPServer(server_address, MyHandler)

    def start_serving(self):
        print('starting SynchronizerAPI server on {}:{}'.format(self.server_address[0], self.server_address[1]))
        self.server.serve_forever()
