#!/usr/bin/env python
import os
import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from Email_Component import Email_Component
from HTTP_Component.htmlReader_MK_2 import Sensor


def getStorageCheckmarks():
    try:
        fileObj = open("enabled_sensors.txt", "r")
    except:
        print("Cannot find enabled_sensors.txt")
        return []

    outList = fileObj.read().split('\n')
    fileObj.close()

    return outList


def writeStorageCheckmarks(checkmarksList):
    try:
        fileObj = open("enabled_sensors.txt", "w")
    except:
        print("Cannot write to enabled_sensors.txt")

    l = len(checkmarksList)

    if(l == 0):
        fileObj.write("")
        print("Wrote nothing.")

    for i in range(l):
        if(i != l-1):
            fileObj.write(checkmarksList[i] + '\n')
        else:
            fileObj.write(checkmarksList[i])

    fileObj.close()


colors = {"background": "343434"}
app = dash.Dash(__name__)

app.layout = html.Div(
        style={"backgroundColor": colors["background"]},
    children=[
        html.Div(
            id="title",
            children=html.H1(children="Home Sensor Suite"),
            style={"textAlign": "center"},
        ),
        html.Div(
            id="major_container1",
            style={'columnCount': 2},
            children=[
                html.Div(
                    id="retrieve-email",
                    style={
                        "width": "100%", 
                        "display" : "inline-block"
                        },
                    children=[
                        html.H3(children='Send test email'),
                        dcc.Input(
                            id="remote-email",
                            placeholder="Input email for raspberry pi",
                            type="text",
                            value="",
                            children=[html.Div(["Input email for raspberry pi"])],
                            style={
                                "width": "95%",
                                "height": "40px",
                                "borderWidth": "1px",
                            },
                        ),
                        html.Button("Submit", id="button"),
                        html.Div(id='output-sensor-readings'),
                    ],
                ),
                html.Div(
                    id="checkboxes_container",
                    style={
                        "width": "100%", 
                        "display": "inline-block",
                        "textAlign": "left",
                        },
                    children=[
                        html.H3(children='Enabled Sensors'),
                        dcc.Checklist(
                            id='enabled-sensors',
                            persistence=True,
                            options=[
                                {'label': 'Temperature', 'value': 'tempSensor'},
                                {'label': 'Humidity', 'value': 'humidSensor'},
                            ],
                            value=getStorageCheckmarks(), # initially enabled
                            labelStyle={
                                'display': 'block', 
                                'textAlign': 'justify',
                            },
                        ),
                        html.Button("Save Selection", id='save-checkmarks-button')
                    ]
                ),
            ]
        )
    ],
)


@app.callback(
        Output(component_id="remote-email", component_property="value"),
        Input(component_id="button", component_property="n_clicks_timestamp"),
        State(component_id="remote-email", component_property="value"),
)
def handle_email(button_timestamp, email):
    if(button_timestamp != None):
        try:
            print("Sending a test email to " + email)
            confirmation = Email_Component(email)

            print(confirmation.confirmation_email())
        except:
            print("Error: Unable to send a test email to " + email)

        return ""
    else:
        return dash.no_update


@app.callback(
        [   # components that will be modified
            Output('enabled-sensors', 'value'),
            Output('output-sensor-readings', 'children'),
        ],
        [   # components to listen for to run the callback
            Input('save-checkmarks-button', 'n_clicks_timestamp'),
        ],
        [   # components to get the state of upon callaback
            State('enabled-sensors', 'value'),
        ],
)
def handle_sensor_toggle(button_timestamp, enabledSensorsList):
    if(button_timestamp != None):
        writeStorageCheckmarks(enabledSensorsList)

        sensor_readings = ""
        if(not enabledSensorsList):
            sensor_readings = dash.no_update

        for sensor in enabledSensorsList:
            if(sensor == "tempSensor"):
                sensor_readings += "Tempurature: " + str(Sensor("temperature").getSensorValue())
            if(sensor == "humidSensor"):
                sensor_readings += "Humidity: " + str(Sensor("humidity").getSensorValue())
            sensor_readings += ' '

        return [enabledSensorsList, sensor_readings]
    else:
        return [getStorageCheckmarks(), dash.no_update]


if __name__ == "__main__":
    app.run_server(debug=True)
