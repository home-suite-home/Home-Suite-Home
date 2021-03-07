#
#   Date: 2/20/21
#   File Name: sensorSim_random.py
#
#   Engineer: Wyatt Vining
#   Contact: wyatt.vining@knights.ucf.edu
#
#   Description:
#       Random values for temperature and humidity are returned to verify UI is updating.
#       The purpose of this script is to simulate a sensor so that we may preform tests of other code without physically having a sensor.
#       This script creates a basic HTTP web server.
#       The server posts a random temperature and humidity when requested.
#       The format is matched to the format of the sesnsor arduinos.
#
#   Important Note:
#       This code is not intended for distrobution.
#       Authorized use for testing perposes only.
#
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random

hostName = "localhost"
serverPort = 8080 # change port if needed - remember to update the port in the recieving script

class SensorSim(BaseHTTPRequestHandler):


    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        randomTemperature = round(random.uniform(15, 30), 2)
        randomHumidity = round(random.uniform(31, 100), 2)

        if self.path == "/temperature":
            self.wfile.write(bytes("%s" % randomTemperature, "utf-8"))
            print("Random Temperature: ", randomTemperature)
        elif self.path == "/humidity":
            self.wfile.write(bytes("%s" % randomHumidity, "utf-8"))
            print("Random Humidity: ", randomHumidity)
        elif self.path == "/fail":
            self.wfile.write(bytes("This test will fail.", "utf-8"))
            print("Failing test sent.")


if __name__ == "__main__":

    webServer = HTTPServer((hostName, serverPort), SensorSim)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
