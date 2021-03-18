from Server_Component.Database import Database
from EmailComponent.EmailController import EmailController
from settings import Settings
import timeKeeper

RATE_LIMIT_DEFAULT = 15
DEVICE_EMAIL = "home.suite.home.test.user@gmail.com"

class Alert:

    def __init__(self, sensor_record, sensorValue):
        self.record = sensor_record
        self.sensor_value = sensorValue
        self.rate_limit = Settings().get_int_setting("alerts", "rate_limit")
        if self.rate_limit >= 0:
            self.rate_limit = RATE_LIMIT_DEFAULT

    def __generate_subject():
        subject = "Out of Tollerace Alert: "
        subject += self.record["name"]
        subject += " Value: "
        subject += self.sensor_value

    def __generate_text_body():
        body += "\nSensor Value Out of Tollerance\n\n"

        body += TimeStamps.getTimestampString()

        body += "\n\nName: "
        body += self.record["name"]
        body += "\nType: "
        body += self.record["type"]
        body += "\nCategory: "
        body += self.record["category"]

        body += "\n\nCurrent Value: "
        body += self.sensor_value
        body += "\nMax Threshold: "
        body += str(self.record["max_threshold"])
        body += "\nMin Threshold: "
        body += str(self.record["min_threshold"])

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
        # TODO - modify __generate_text_body() to follow HTML format
        return ""

    def sendAlert(self):
        db = Database()

        if db.alertSent(self.record["name"], self.record["type"], self.rate_limit) is True:
            return None
        else:
            db.saveLog(self.record["name"], self.record["type"])
            
            subject = self.__generate_subject()
            body_text = self.__generate_text_body()
            body_html = self.__generate_html_body()

            users = db.getAllUsers()

            for user in users:
                email = EmailController(user["email"], DEVICE_EMAIL)
                message = email.compose_email(subject, body_text, body_html)
                email.send_email(message)
