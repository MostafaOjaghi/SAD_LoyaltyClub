from http.server import BaseHTTPRequestHandler, HTTPServer
from db.DB import DBClass
from PD.PointsDefinition import PointsDefinition


class PointsDefinitionHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            # getting parameters
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)  # <--- Gets the data itself
            params = dict([tuple(s.split("=")) for s in post_data.decode("utf-8").split("&")])
            # print(params)
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
            # getting parameters
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)  # <--- Gets the data itself
            params = dict([tuple(s.split("=")) for s in post_data.decode("utf-8").split("&")])
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
            # getting parameters
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)  # <--- Gets the data itself
            params = dict([tuple(s.split("=")) for s in post_data.decode("utf-8").split("&")])
            # print(params)
        except:
            self.send_error(400, "no parameters sent")
            print("no parameters sent")
            return
        if self.path == "/rank":
            self.handle_update_rank(params)

    def do_GET(self):
        content_length = self.headers['Content-Length']
        print(content_length)
        if content_length is None:
            # return all scores

            return

        content_length = int(content_length)  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        params = dict([tuple(s.split("=")) for s in post_data.decode("utf-8").split("&")])
        if len(params) > 1:
            self.send_error(400, "too many parameters")
            print("too many parameters")
            return
        if "id" not in params:
            self.send_error(400, "wrong parameters")
            print("wrong parameters")
            return

        # user_order = PointsDefinitionHandler.DB.
        # score = PointsDefinitionHandler.PD.cal_score(user_order)
        # send score to sale system

        # print(params)
        return

    def handle_update_rank(self, params):
        have_name = PointsDefinitionHandler.fields_in_params(params, ["name"])
        have_range = PointsDefinitionHandler.fields_in_params(params, ["rank_range"])
        have_off = PointsDefinitionHandler.fields_in_params(params, ["off"])
        have_limit = PointsDefinitionHandler.fields_in_params(params, ["monthly_limit"])
        have_freeshipping = PointsDefinitionHandler.fields_in_params(params, ["free_shipping"])
        total_correct_params = have_name + have_range + have_off + have_limit + have_freeshipping
        if len(params) > total_correct_params:
            self.send_error(400, "too many parameters")
            print("too many parameters")
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
                    print(self.PD.ranks)
                    rank["rank range"] = rank_range
                    rank["off"] = off
                    rank["monthly limit"] = monthly_limit
                    rank["free shipping"] = free_shipping
                    print(self.PD.ranks)
                    self.send_response(200)
                    self.end_headers()
                except:
                    self.send_error(400, "wrong parameters format")
                    print("wrong parameters format")
        return

    def handle_add_rank(self, params):
        if PointsDefinitionHandler.fields_in_params(params, ["name", "rank_range", "off",
                                                             "monthly_limit", "free_shipping"]):
            print(params)
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

                print(self.PD.ranks)
                self.PD.ranks[name] = {
                    "rank range": rank_range,
                    "off": off,
                    "monthly limit": monthly_limit,
                    "free shipping": free_shipping
                }
                print(self.PD.ranks)
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
        if len(params) > 2:
            self.send_error(400, "too many parameters")
            print("too many parameters")
            return
        have_score_coefficient = PointsDefinitionHandler.fields_in_params(params, ["score_coefficient"])
        have_score_period = PointsDefinitionHandler.fields_in_params(params, ["score_period"])

        if have_score_coefficient and have_score_period:
            self.PD.score_coefficient = params["score_coefficient"]
            self.PD.score_period = params["score_period"]
            self.send_response(200)
            self.end_headers()

        elif len(params) == 1:
            if have_score_coefficient:
                self.PD.score_coefficient = params["score_coefficient"]
                self.send_response(200)
                self.end_headers()
            elif have_score_period:
                self.PD.score_coefficient = params["score_period"]
                self.send_response(200)
                self.end_headers()
            else:
                self.send_error(400, "wrong parameter")
                print("wrong parameters")
        else:
            self.send_error(400, "wrong parameters")
            print("wrong parameters")
        return
        # save score_period

    @staticmethod
    def fields_in_params(params, fields):
        for field in fields:
            if field not in params:
                return False
        return True


class PointsDefinitionAPI:
    def __init__(self, server_address, DB, PD):
        PointsDefinitionHandler.DB = DB
        PointsDefinitionHandler.PD = PD
        self.server_address = server_address
        self.server = HTTPServer(server_address, PointsDefinitionHandler)

    def start_serving(self):
        print('starting server on {}:{}'.format(self.server_address[0], self.server_address[1]))
        self.server.serve_forever()


s = PointsDefinitionAPI(('127.0.0.1', 8081), "DB", PointsDefinition("DB"))
s.start_serving()
