from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib
import ast


class PointsDefinitionHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            params = self.get_params()
            print(params)
        except:
            self.send_error(400, "no parameters sent")
            print("no parameters sent")
            return

        if self.path == "/score-parameters":
            self.handle_score_parameter(params)
        elif self.path == "/rank":
            self.handle_add_rank(params)
        return

    def do_DELETE(self):
        try:
            params = self.get_params()
            # print(params)
        except:
            self.send_error(400, "no parameters sent")
            print("no parameters sent")
            return
        if self.path == "/rank":
            if len(params) != 1:
                self.send_error(400, "too many parameters")
                print("too many parameters")
            elif not PointsDefinitionHandler.fields_in_params(params, ["name"]):
                self.send_error(400, "wrong parameters")
                print("wrong parameters")
            else:
                name = params["name"]
                if name not in self.PD.ranks:
                    self.send_error(400, "no rank with this name")
                    print("no rank with this name")
                else:
                    print(self.PD.ranks)
                    del self.PD.ranks[name]
                    print(self.PD.ranks)
                    self.send_response(200)
                    self.end_headers()
        return

    def do_PUT(self):
        try:
            params = self.get_params()
            # print(params)
        except:
            self.send_error(400, "no parameters sent")
            print("no parameters sent")
            return
        if self.path == "/rank":
            self.handle_update_rank(params)

    def do_GET(self):
        try:
            params = self.get_params()
            # print(params)
        except:
            if self.path == "/rank":
                self.send_ranks()
                return
            elif self.path == "/annual-income":
                self.handle_annual_income()
                return
            else:
                self.send_error(400, "no parameters sent")
                print("no parameters sent")
                return

        if self.path == "/customers-score":
            self.handle_customer_ids(params)
        elif self.path == "/rank-info":
            self.handle_rank_info(params)
        elif self.path == "/rank":
            self.handle_rank(params)
        return

    def send_ranks(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        json_string = json.dumps(self.PD.ranks)
        self.wfile.write(bytes(json_string, 'utf-8'))
        return

    def get_params(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        params = dict([tuple(s.split("=")) for s in post_data.decode("utf-8").split("&")])
        return params

    def handle_annual_income(self):
        sales = self.PD.get_last_years_sales()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        json_string = json.dumps(sales)
        self.wfile.write(bytes(json_string, 'utf-8'))

    def handle_rank(self, params):
        if PointsDefinitionHandler.fields_in_params(params, ["customer_ids"]):
            if len(params) > 1:
                self.send_error(400, "too many parameters")
                print("too many parameters")
            else:
                customer_ids = urllib.parse.unquote(params["customer_ids"])
                customer_ids = ast.literal_eval(customer_ids)
                ranks = self.PD.get_users_ranks(customer_ids)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                json_string = json.dumps(ranks)
                self.wfile.write(bytes(json_string, 'utf-8'))
        elif PointsDefinitionHandler.fields_in_params(params, ["first", "last"]):
            if len(params) > 2:
                self.send_error(400, "too many parameters")
                print("too many parameters")
            else:
                first = int(params["first"])
                last = int(params["last"])
                ranks = self.PD.get_rank_range(first, last)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                json_string = json.dumps(ranks)
                self.wfile.write(bytes(json_string, 'utf-8'))

        return

    def handle_rank_info(self, params):
        if PointsDefinitionHandler.fields_in_params(params, ["customer_ids"]):
            if len(params) > 1:
                self.send_error(400, "too many parameters")
                print("too many parameters")
            else:
                customer_ids = urllib.parse.unquote(params["customer_ids"])
                customer_ids = ast.literal_eval(customer_ids)
                ranks_info = self.PD.get_rank_info(customer_ids)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                json_string = json.dumps(ranks_info)
                self.wfile.write(bytes(json_string, 'utf-8'))
        else:
            self.send_error(400, "wrong parameters")
            print("wrong parameters")

    def handle_customer_ids(self, params):
        if PointsDefinitionHandler.fields_in_params(params, ["customer_ids"]):
            if len(params) > 1:
                self.send_error(400, "too many parameters")
                print("too many parameters")
            else:

                customer_ids = urllib.parse.unquote(params["customer_ids"])
                customer_ids = ast.literal_eval(customer_ids)
                # get customer scores from DB
                customer_scores = {}
                for id in customer_ids:
                    customer_scores[id] = self.DB.get_customer_score(id)[0]
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                json_string = json.dumps(customer_scores)
                self.wfile.write(bytes(json_string, 'utf-8'))

        elif PointsDefinitionHandler.fields_in_params(params, ["recalculate_ids"]):
            if len(params) > 1:
                self.send_error(400, "too many parameters")
                print("too many parameters")
            else:
                customer_ids = urllib.parse.unquote(params["recalculate_ids"])
                customer_ids = ast.literal_eval(customer_ids)
                customer_scores = self.PD.cal_users_scores(customer_ids)
                customer_scores = dict([(customer_ids[i], customer_scores[i]) for i in range(len(customer_ids))])
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                json_string = json.dumps(customer_scores)
                self.wfile.write(bytes(json_string, 'utf-8'))
        else:
            self.send_error(400, "wrong parameters")
            print("wrong parameters")

    def handle_update_rank(self, params):
        have_name = PointsDefinitionHandler.fields_in_params(params, ["name"])
        have_range = PointsDefinitionHandler.fields_in_params(params, ["rank_range"])
        have_off = PointsDefinitionHandler.fields_in_params(params, ["off"])
        have_limit = PointsDefinitionHandler.fields_in_params(params, ["monthly_limit"])
        have_freeshipping = PointsDefinitionHandler.fields_in_params(params, ["free_shipping"])
        total_correct_params = have_name + have_range + have_off + have_limit + have_freeshipping
        if len(params) != total_correct_params:
            self.send_error(400, "wrong parameters")
            print("wrong parameters")
        elif not have_name or params["name"] == "":
            self.send_error(400, "should specify rank name")
            print("should specify rank name")
        else:
            if params["name"] not in self.PD.ranks:
                self.send_error(400, "no rank with this name")
                print("no rank with this name")
            else:
                try:
                    name = params["name"]
                    rank = self.PD.ranks[name]
                    rank_range, off, monthly_limit, free_shipping = rank["rank range"], rank["off"], rank["monthly limit"], rank["free shipping"]
                    if have_range:
                        rank_range = [float(x) for x in params["rank_range"].split("_")]
                        if len(rank_range) != 2:
                            raise Exception()
                    if have_off:
                        off = float(params["off"])
                    if have_limit:
                        monthly_limit = float(params["monthly_limit"])
                    if have_freeshipping:
                        free_shipping = params["free_shipping"]
                        if free_shipping == "true" or free_shipping == "false":
                            free_shipping = True if params["free_shipping"] == "True" else False
                        else:
                            raise Exception()
                    rank["rank range"] = rank_range
                    rank["off"] = off
                    rank["monthly limit"] = monthly_limit
                    rank["free shipping"] = free_shipping
                    self.send_response(200)
                    self.end_headers()
                except:
                    self.send_error(400, "wrong parameters format")
                    print("wrong parameters format")
        return

    def handle_add_rank(self, params):
        if PointsDefinitionHandler.fields_in_params(params, ["name", "rank_range", "off",
                                                             "monthly_limit", "free_shipping"]):
            if len(params) > 5:
                self.send_error(400, "too many parameters")
                print("too many parameters")
                return

            elif len(params) < 5:
                self.send_error(400, "too few parameters")
                print("too few parameters")
                return

            try:
                name = params["name"]
                rank_range = [float(x) for x in params["rank_range"].split("_")]
                off = float(params["off"])
                monthly_limit = float(params["monthly_limit"])
                free_shipping = params["free_shipping"]
                if free_shipping == "true" or free_shipping == "false":
                    free_shipping = True if params["free_shipping"] == "True" else False
                else:
                    raise Exception()
                if name == "" or len(rank_range) != 2:
                    raise Exception()
                if name in self.PD.ranks:
                    self.send_error(400, "rank with this name already exists")
                    print("rank with this name already exists")
                    return
                self.PD.ranks[name] = {
                    "rank range": rank_range,
                    "off": off,
                    "monthly limit": monthly_limit,
                    "free shipping": free_shipping
                }
                self.send_response(200)
                self.end_headers()
                return

            except:
                self.send_error(400, "wrong parameters format")
                print("wrong parameters format")
                return

        else:
            self.send_error(400, "too few parameters")
            print("too few parameters")
            return

    def handle_score_parameter(self, params):
        have_score_coefficient = PointsDefinitionHandler.fields_in_params(params, ["score_coefficient"])
        have_score_period = PointsDefinitionHandler.fields_in_params(params, ["score_period"])
        have_max_order_score = PointsDefinitionHandler.fields_in_params(params, ["max_order_score"])
        total_correct_parameters = have_score_coefficient + have_score_period + have_max_order_score

        if len(params) != total_correct_parameters:
            self.send_error(400, "wrong parameters")
            print("wrong parameters")
            return
        try:
            score_coefficient, score_period, max_order_score = self.PD.score_coefficient, self.PD.score_period, self.PD.max_order_score
            if have_score_coefficient:
                score_coefficient = float(params["score_coefficient"])
            if have_score_period:
                score_period = int(params["score_period"])
            if have_max_order_score:
                max_order_score = float(params["max_order_score"])
            self.PD.score_coefficient = score_coefficient
            self.PD.score_period = score_period
            self.PD.max_order_score = max_order_score
            self.send_response(200)
            self.end_headers()
        except:
            self.send_error(400, "wrong parameters format")
            print("wrong parameters format")

    @staticmethod
    def fields_in_params(params, fields):
        for field in fields:
            if field not in params:
                return False
        return True

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPRequestHandler.end_headers(self)


class PointsDefinitionAPI:
    def __init__(self, server_address, DB, PD):
        PointsDefinitionHandler.DB = DB
        PointsDefinitionHandler.PD = PD
        self.server_address = server_address
        self.server = HTTPServer(server_address, PointsDefinitionHandler)

    def start_serving(self):
        print('starting PointsDefinitionAPI server on {}:{}'.format(self.server_address[0], self.server_address[1]))
        self.server.serve_forever()
