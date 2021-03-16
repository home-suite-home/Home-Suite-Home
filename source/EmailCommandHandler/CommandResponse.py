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

        elif "get sensor data:" in self.command:
            sensor_rqst = self.command.split(":", 1)[1]
            sensor_rqst = sensor_rqst.split(",")
            sensor_type = sensor_rqst[0].strip()
            sensor_name = sensor_rqst[1].strip()
            sensor_time = sensor_rqst[2].strip()
            return sensor_data_analytics(sensor_type, sensor_name, sensor_time)


        else:
            return help_message()

###############################################################################
'''
Response definitions
'''
###############################################################################

def help_message():
    text_response = "dummy help message"
    html_response = """\
    <html>
        <body>
            <p>help message<br>
                <p>
                    COMMAND                               |   RESPONSE                            <br>
                    get most recent sensor data           | recieve the most recent data          <br>
                                                          | for each sensor by name               <br>
                    get sensor data: <name>, <yryr-mn-dy> | recieve all data from sensor <name>   <br>
                                                          | including from <date> until current   <br>
                                                          | time                                  <br>
                </p>
            </p>
        </body>
    </html>
    """
    return (text_response, html_response, None)

def sensor_data_analytics(type, name, days):
    import sys
    # translates to the Home-Suite-Home/Source directory
    sys.path.append("..")
    sys.path.append("../AnalyticsComponent")
    import LineGraph
    from timeKeeper import TimeStamps

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
    import sys
    # translates to the Home-Suite-Home/Source directory
    sys.path.append("../Server_Component")
    from Database import Database
    url = 'localhost'
    port = 27017

    # instantiate database and connect
    db = Database(url, port)
    db.connect()

    # only grab sensors with configs
    config_list = db.getConfigData()
    name_list = []
    type_list = []
    for config in config_list:
        name_list.append(config["name"])
        type_list.append(config["type"])

    # retrieve data from db
    data_list = []
    for i in range(len(config_list)):
        data_list.append(db.getRecentSensorData(name_list[i], type_list[i], 1))

    # get most recent of these lists
    most_recent_list = []
    for sub_list in (data_list):
        most_recent_list.append(sub_list[0])

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
    for sensor in most_recent_list:
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
    text_response = str(most_recent_list)

    # TESTING
    db.clear()
    return (text_response, html_table, None)
