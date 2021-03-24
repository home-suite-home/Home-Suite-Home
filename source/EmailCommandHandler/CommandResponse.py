'''
//
//  Date: 02/18/2021
//  FileName: CommandResponse.py
//
//  Engineer: David Crumley
//  Contact: david_crumley@knights.ucf.edu
//
//  Description:
        will output appropriate response based on incoming command
        will handle accessing the database for sensor data


 *************************************************************
 || - TODO: add enabled_sensors.txt functionality           ||
 ||         - only want to display sensors that are enabled ||
 *************************************************************
'''

import sys
# translates to the Home-Suite-Home/Source directory
sys.path.append("..")
from Server_Component.Database import Database
from AnalyticsComponent.LineGraph import *
from timeKeeper import TimeStamps
from settings import Settings

url = 'localhost'
port = 27017


class CommandResponse:
    def __init__ (self, command):
        self.command = command

    def get_response(self):
        if self.command == "help":
            return help_message()

        elif self.command == "get most recent sensor data":
            return most_recent_data()

        elif "get sensor data:" in self.command:
            sensor_rqst = self.command.split(":", 1)[1]
            sensor_rqst = sensor_rqst.split(",")
            sensor_type = sensor_rqst[0].strip()
            sensor_name = sensor_rqst[1].strip()
            print(sensor_name)
            sensor_time = sensor_rqst[2].strip().split("\r\n")[0]
            return sensor_data_analytics(sensor_type, sensor_name, sensor_time)

        elif self.command == "silence alerts":
            return alerts_silenced()

        elif self.command == "resume alerts":
            return alerts_resumed()

        else:
            return help_message()

###############################################################################
'''
Response definitions
'''
###############################################################################

def alerts_silenced():
    s = Settings()

    curr = s.get_bool_setting('alerts', 'silence_alerts')
    if curr:
        text_response = "Alerts already silenced"
    else:
        success = s.set_setting('alerts', 'silence_alerts', 'True')
        if success:
            text_response = "Alerts silenced"
        else:
            text_response = "Unable to silence alerts"

    return (text_response, None, None)

def alerts_resumed():
    s = Settings()

    curr = s.get_bool_setting('alerts', 'silence_alerts')
    if not curr:
        text_response = "Alerts already on"
    else:
        success = s.set_setting('alerts', 'silence_alerts', 'False')
        if success:
            text_response = "Alerts are on"
        else:
            text_response = "Unable to resume alerts"

    return (text_response, None, None)

def help_message():
    text_response = "Please review command options"
    html_response = """\
        <html>
        <head>
        <style>
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
            }

        td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even) {
            background-color: #dddddd;
        }
        </style>
        </head>
        <body>

        <h2>Home-Suite-Home Email Command Options</h2>

        <table>
            <tr>
                <th>Command</th>
                <th>Response</th>
            </tr>
            <tr>
                <td>help</td>
                <td>Return this help table</td>
            </tr>
            <tr>
                <td>get most recent sensor data</td>
                <td>Return a table containing the most recent data for each sensor</td>
            </tr>
            <tr>
                <td>get sensor data: <sensor type>, <sensor name>, <hours></td>
                <td>Return a graph displaying sensor data over a period of <hours></td>
            </tr>
            <tr>
                <td>silence alerts</td>
                <td>Email alerts for all sensors will be silenced</td>
            </tr>
            <tr>
                <td>resume alerts</td>
                <td>Email alerts for all sensors will be resumedS</td>
            </tr>
    """

    return (text_response, html_response, None)

def sensor_data_analytics(type, name, days):

    hours = int(days)*24

    # create line graph
    graph = LineGraph.data_over_time(type, name, hours)
    # check for empty graph
    if not graph:
        return help_message()

    ts = TimeStamps()
    # create filename
    filepath = "../../analytics/"
    filename = "command_response_"
    filename += str(ts.getTimestamp())
    filename += ".png"
    filepath += filename
    graph.write_image(filepath)

    return(name, "Sensor data over time", filepath)



def most_recent_data():
    '''
    use the getData() function provided by Database.py
     - getData returns a dict of all data currently in the database
     - data written to a temp.txt file to avoid memory starvation

     - TODO: add enabled_sensors.txt functionality
             - only want to display sensors that are enabled
    '''
    # instantiate database and connect
    db = Database(url, port)
    db.connect()

    # only grab sensors with configs
    config_list = db.getConfigData()

    # get most recent of these lists
    most_recent_list=[]
    for sensor in (config_list):
        most_recent_list.append(db.getMostRecentSensorData(sensor["name"], sensor["type"]))

    # html string common to all tables
    html_table = """\
        <html>
        <head>
        <style>
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
            }

        td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even) {
            background-color: #dddddd;
        }
        </style>
        </head>
        <body>

        <h2>Most Recent Sensor Data</h2>

        <table>
            <tr>
                <th>Sensor Type</th>
                <th>Sensor Name</th>
                <th>Sensor Value</th>
            </tr>
    """

    # create the table based on sensor_list data
    i = 0
    for sensor in config_list:
        data = most_recent_list[i]
        html_table += """\
            <tr>
                <td>{sensor[type]}</td>
                <td>{sensor[name]}</td>
                <td>{data}</td>
            </tr>
            """.format(**locals())
        i += 1


    # add the html trailers
    html_table += """\
        </table>
        </body>
        </html>
        """
    text_response = str(most_recent_list)

    return (text_response, html_table, None)
