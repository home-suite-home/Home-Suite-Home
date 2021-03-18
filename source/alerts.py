from Server_Component.Database import Database
from EmailComponent.EmailController import EmailController
from settings import Settings
import timeKeeper
from conversions import Units

RATE_LIMIT_DEFAULT = 15
#DEVICE_EMAIL = "home.suite.home.test.user@gmail.com"

class Alert:

    def __init__(self, sensor_record, sensorValue):
        self.record = sensor_record

        self.sensor_value = sensorValue

        self.rate_limit = Settings().get_int_setting("alerts", "rate_limit")
        if self.rate_limit <= 0:
            self.rate_limit = RATE_LIMIT_DEFAULT

        units = Units(self.record["type"], self.record["units"])
        self.sensor_value = units.convert(self.sensor_value)
        self.min_threshold = units.convert(self.record["min_threshold"])
        self.max_threshold = units.convert(self.record["max_threshold"])

    def __generate_subject(self):
        subject = "Out of Tolerace Alert: "
        subject += self.record["name"]
        subject += " Value: "
        subject += str(self.sensor_value)
        return subject

    def __generate_text_body(self):
        body = "\nSensor Value Out of Tolerance\n\n"

        body += timeKeeper.TimeStamps().getTimestampString()

        body += "\n\nName: "
        body += self.record["name"]
        body += "\nType: "
        body += self.record["type"]
        body += "\nCategory: "
        body += self.record["category"]

        body += "\n\nCurrent Value: "
        body += str(self.sensor_value)
        body += "\nMax Threshold: "
        body += str(self.max_threshold)
        body += "\nMin Threshold: "
        body += str(self.min_threshold)

        body += "\n\nSensor Settings:"
        body += "\nIP Address: "
        body += self.record["address"]
        body += "\nPort: "
        body += str(self.record["port"])
        body += "\nSub Address: /"
        body += self.record["sub_address"]
        body += "\nUnits: "
        body += self.record["units"]
        body += "\nAlerts: "
        body += str(self.record["alerts"])
        body += "\n\n"

        return body

    def __generate_html_body(self):
        body = """
            <html>
            <body>
            """

        body += "<h1>Sensor Value Out of Tolerance</h1>"

        body += "<h2>"
        body += timeKeeper.TimeStamps().getTimestampString()
        body += "</h2>"

        body += "<h2>Name: "
        body += self.record["name"]
        body += "<br>Current Value: "
        body += str(self.sensor_value)
        body += "<br>Max Threshold: "
        body += str(self.max_threshold)
        body += "<br>Min Threshold: "
        body += str(self.record["min_threshold"])
        body += "</h2></p>"

        body += "<p><br><h3>Sensor Configuration</h3>"
        body += "<h4>Type: "
        body += self.record["type"]
        body += "<br>Category: "
        body += self.record["category"]
        body += "<br>IP Address: "
        body += self.record["address"]
        body += "<br>Port: "
        body += str(self.record["port"])
        body += "<br>Sub Address: /"
        body += self.record["sub_address"]
        body += "<br>Units: "
        body += self.record["units"]
        body += "<br>Alerts: "
        body += str(self.record["alerts"])
        body += "</h4></p></body></html>"

        return body

    def handleAlert(self):
        db = Database()

        if db.alertSent(self.record["name"], self.record["type"], self.rate_limit) is True:
            return None
        else:
            subject = self.__generate_subject()
            body_text = self.__generate_text_body()
            body_html = self.__generate_html_body()

            users = db.getAllUsers()

            for user in users:
                #email = EmailController(user["email"], DEVICE_EMAIL)
                email = EmailController(user["email"])
                message = email.compose_email(subject, body_text, body_html)
                email.send_email(message)
                print("email sent to: ", user["email"])

            db.saveLog(self.record["name"], self.record["type"])
