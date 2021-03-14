from EmailComponent.EmailController import EmailController
import timeKeeper

class Alert:

    def __init__(self, sensor_record, sensorValue):
        record = self.sensor_record
        sensor_value = self.sensorValue

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

    def __save_alert_to_log(self):
        # TODO - save alert to history database object
        pass

    def sendAlert(self):
        # TODO:
            # integrate encryption.py into EmailController
            # Create a way to itterate over multiple user email addresses ??
        email = EmailController()

        subject = self.__generate_subject()
        body_text = self.__generate_text_body()
        body_html = self.__generate_html_body()

        message = email.compose_email(subject body_text, body_html)

        email.send_email(message)
