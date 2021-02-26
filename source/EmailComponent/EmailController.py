
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

class CommandResponse:
    def __init__ (self, command):
        self.command = command

    def get_response(self):
        if self.command == "help":
            return help_message()

        elif self.command == "get most recent sensor data":
            return most_recent_data()

        else:
            return help_message()

###############################################################################
'''
Response definitions
'''
###############################################################################

def help_mesasage():
    text_response = "dummy help message"
    html_response = """\
    <html>
        <body>
            <p>dummy help message<br>
                <a href="https://github.com/home-suite-home/Home-Suite-Home">
                heres a link to the github, figure it out</a>
            </p>
        </body>
    </html>
    """
    return (text_response, html_response)

def most_recent_data():
    '''
    use the getData() function provided by Database.py
     - getData returns a dict of all data currently in the database
     - data written to a temp.txt file to avoid memory starvation

     - TODO: add enabled_sensors.txt functionality
             - only want to display sensors that are enabled
    '''
    import sys
    # translates to the Home-Suite-Home/Source directory
    sys.path.append("../Server_Component")
    from Database import Database
    url = 'localhost'
    port = 27017

    # instantiate database and connect
    db = Database(url, port)
    db.connect()

    ### TESTING ###
    db.SendSensorData(38.0, "temp_1", "Temp")
    db.SendSensorData(15.0, "temp_2", "Temp")
    db.SendSensorData(37.0, "temp_1", "Temp")
    db.SendSensorData(10.0, "temp_3", "Temp")

    # retrieve data from db
    data_list = db.GetData()

    # search for each sensor name and retrieve latest entry
    name_list = []
    sensor_list = []
    for data_obj in reversed(data_list):
        if data_obj["name"] not in name_list:
            name_list.append(data_obj["name"])
            sensor_list.append(data_obj)

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
    for sensor in sensor_list:
        html_table += """\
            <tr>
                <td>{sensor[type]}</td>
                <td>{sensor[name]}</td>
                <td>{sensor[value]}</td>
            </tr>
            """.format(**locals())


    # add the html trailers
    html_table += """\
        </table>
        </body>
        </html>
        """
    text_response = str(data_list)

    # TESTING
    db.Clear()
    return (text_response, html_table)
