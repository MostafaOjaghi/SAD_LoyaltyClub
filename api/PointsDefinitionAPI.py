from http.server import BaseHTTPRequestHandler, HTTPServer
from db.DB import DBClass
from PD.PointsDefinition import PointsDefinition


class PointsDefinitionHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # print("params", self.PD.params)
        # print("modes: ", self.PD.modes)

        try:
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)  # <--- Gets the data itself
            params = dict([tuple(s.split("=")) for s in post_data.decode("utf-8").split("&")])
        except:
            self.send_error(400, "no parameters sent")
            print("no parameters sent")
            return

        if PointsDefinitionHandler.fields_in_params(params, ["interval", "mode"]):
            items = list(params.items())
            if len(items) > 5:
                self.send_error(400, "too many parameters")
                print("too many parameters")
                return
            try:
                mode = int(params["mode"])
                interval = int(params["interval"])
            except:
                self.send_error(400, "interval and mode should be integers")
                print("interval and mode should be integers")
                return
            try:
                pd_params = [float(x) for x in ([params.get("a")] + [params.get("b")] + [params.get("k")]) if x is not None]
            except:
                self.send_error(400, "parameters should be float")
                print("parameters should be float")
                return


            if mode == 0:
                if PointsDefinitionHandler.fields_in_params(params, ["a", "b", "k"]):
                    PointsDefinitionHandler.PD.modes[interval] = mode
                    PointsDefinitionHandler.PD.params[interval] = pd_params
                else:
                    self.send_error(400, "mode 0 parameters : a, b, k")
                    # print("too few parameters")
                    return
            elif mode == 1:
                if "a" in params and len(items) == 3:
                    PointsDefinitionHandler.PD.modes[interval] = mode
                    PointsDefinitionHandler.PD.params[interval] = pd_params
                else:
                    self.send_error(400, "mode 1 parameters : a")
                    # print("mode 1 parameters : a")
                    return
            elif mode == 2:
                if PointsDefinitionHandler.fields_in_params(params, ["a", "b"]) and len(items) == 4:
                    PointsDefinitionHandler.PD.modes[interval] = mode
                    PointsDefinitionHandler.PD.params[interval] = pd_params
                else:
                    self.send_error(400, "mode 2 parameters : a, b")
                    # print("mode 2 parameters : a, b")
                    return
            else:
                self.send_error(400, "mode should be 0, 1 or 2")
                # print("mode should be 0, 1 or 2")
                return

            self.send_response(200)
            self.end_headers()
            # print("params", self.PD.params)
            # print("modes: ", self.PD.modes)
        return

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


s = PointsDefinitionAPI(('127.0.0.1', 8081), "DB", PointsDefinition())
s.start_serving()
