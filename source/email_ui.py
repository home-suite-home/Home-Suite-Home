#!/usr/bin/env python
import os
import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from Email_Component import Email_Component
from HTTP_Component.htmlReader_MK_2 import Sensor


sys.path.append(".")
colors = {"background": "343434"}
app = dash.Dash(__name__ )


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
                            multiple=True,
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
                            options=[
                                {'label': 'Temperature', 'value': 'tempSensor'},
                                {'label': 'Humidity', 'value': 'humidSensor'},
                            ],
                            value=[], # initially enabled
                            labelStyle={
                                'display': 'block', 
                                'textAlign': 'justify',
                                },
                        )
                    ]
                )
            ]
        )
    ],
)


@app.callback(
        [
            Output(component_id="remote-email", component_property="value"),
            Output('enabled-sensors', 'value'),
            Output('output-sensor-readings', 'children'),
        ],
        [
            Input(component_id="button", component_property="n_clicks"),
            Input('enabled-sensors', 'value'),
        ],
        [
            State(component_id="remote-email", component_property="value"),
        ],
)
def update_output(n_clicks, enabledSensorsList, remote_email):
    if(not enabledSensorsList):
        sensor_readings = dash.no_update
    else:
        sensor_readings = ""

    for sensor in enabledSensorsList:
        if(sensor == "tempSensor"):
            sensor_readings += "Tempurature: " + str(Sensor("temperature").getSensorValue())
        if(sensor == "humidSensor"):
            sensor_readings += "Humidity: " + str(Sensor("humidity").getSensorValue())

        sensor_readings += ' '


    if remote_email != "":
        try:
            print("Sending a test email to " + remote_email)
            confirmation = Email_Component(remote_email)

            print(confirmation.confirmation_email())
        except:
            print("Error: Unable to send a test email to " + remote_email)
        
        return ["", enabledSensorsList, sensor_readings]
    else:
        return [dash.no_update, enabledSensorsList, sensor_readings]

    return [dash.no_update, enabledSensorsList, sensor_readings]


if __name__ == "__main__":
    app.run_server(debug=True)
