#!/usr/bin/env python
import os
import sys
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH
from Email_Component import Email_Component
from HTTP_Component.Sensors import Sensor
from UI_Utils import *

sensor_names = {
        # (display name, url extension, units)
        'tempSensor': ('Temperature', 'temperature', 'F'), 
        'humidSensor': ('Humidity', 'humidity', '%')
    }

new_sensor_card = html.Div(className='card',
                    id='new-card',
                    children=[
                        html.H4(''),
                        html.Button('Add New Sensor', id='new-card-button',),
                    ]
                )

new_card_fields = [
    html.H4('New Sensor'),
    html.Div(
        [
            dcc.Input(
                id='field_sensor-name',
                autoFocus=True,
                debounce=True,
                placeholder='Sensor Name',
            ),
            dcc.Input(
                id='field_units',
                debounce=True,
                placeholder='Units',
            ),
            dcc.Input(
                id='field_ip-address',
                debounce=True,
                placeholder='IP Address',
            ),
            dcc.Input(
                id='field_port-number',
                debounce=True,
                placeholder='Port Number (Optional)',
            ),
            dcc.Input(
                id='field_url-plug',
                debounce=True,
                placeholder='URL Plug',
            ),
            daq.BooleanSwitch(
                id='field_alert',
                on=False,
                color='#9ad6aa',
                label='Alerts:',
                labelPosition='top',
            ),
            html.H4(''),
            html.Button('Create', id='field_create-card-button'),
            html.H4('Invalid Selection', style={'display': 'none'}, id='invalid-selection'),
        ],
        #style={'textAlign': 'left'},
    ),
]

fields_card = html.Div(className='card',
                    id='fields-card',
                    children=new_card_fields,
                    style={'display': 'none'},
                )


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

    checkmarksList = [x for x in checkmarksList if x != '']

    l = len(checkmarksList)

    if(l == 0):
        print("Wrote nothing.")

    for i in range(l):
        if(i != l-1):
            fileObj.write(checkmarksList[i] + '\n')
        else:
            fileObj.write(checkmarksList[i])

    fileObj.close()


def getCardDivs(enabledSensorsList):
    divList = []
    enabledSensorsList = [i for i in enabledSensorsList if i] # needs more permanent fix...
    for enabledSensor in enabledSensorsList:
        divList.append(
            html.Div(className='card',
                children=[
                    html.H4(
                        sensor_names[enabledSensor][0],
                    ),
                    html.H2(str(
                        Sensor(sensor_names[enabledSensor][1]).
                        getSensorValue()) + ' ' + 
                        sensor_names[enabledSensor][2],
                        id={'type': 'sensor-data', 'index': enabledSensor},
                    ),
                    html.Button('Refresh',
                        id={'type': 'refresh-button', 'index': enabledSensor},
                    ),
                ]
            )
        )

    #for i in range(12):
    #    divList.append(html.Div(className='card', children=[html.H4('<Test card {}>'.format(i))]))

    divList.append(new_sensor_card)

    return divList


colors = {"background": "343434"}
app = dash.Dash(__name__, suppress_callback_exceptions=True)


mainDivChildren = [
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
                        type="email",
                        value="",
                        children=[html.Div(["Input email for raspberry pi"])],
                        style={
                            "width": "95%",
                            "height": "40px",
                            "borderWidth": "1px",
                        },
                        debounce=True,
                    ),
                    html.Button("Submit", id="button",),
                    #html.Div(id='output-sensor-readings'),
                ],
            ),
            #    html.Div(
            #        id="checkboxes_container",
            #        style={
            #            "width": "100%", 
            #            "display": "inline-block",
            #            "textAlign": "left",
            #            },
            #        children=[
            #            html.H3(children='Enabled Sensors'),
            #            dcc.Checklist(
            #                id='enabled-sensors',
            #                persistence=True,
            #                options=[
            #                    {'label': 'Temperature', 'value': 'tempSensor'},
            #                    {'label': 'Humidity', 'value': 'humidSensor'},
            #                ],
            #                value=getStorageCheckmarks(), # initially enabled
            #                labelStyle={
            #                    'display': 'block', 
            #                    'textAlign': 'justify',
            #                },
            #            ),
            #            html.Button("Save Selection", id='save-checkmarks-button')
            #        ]
            #    ),
        ],
    ),
    html.Div(id="cards-container", 
        style={
            #'overflow': 'auto', 
            #'overflow': 'hidden', 
            'width': '100%', 
            'height': '100%', 
            #'display': 'table', 
            'display': 'grid',
            'align-content': 'start',
            'grid-template-columns': 'repeat(auto-fill, 230px)',
            #'grid-auto-flow': 'column',
            #'border-spacing': '20px', 
            #'table-layout': 'fixed',
            #'position': 'relative',

        },
        children=[fields_card, new_sensor_card,]
    ),
    #html.Button('Create', id='field_create-card-button', hidden=True)
]


app.layout = html.Div(
        style={"backgroundColor": colors["background"]},
        children=mainDivChildren
)


# Email Entry Callback
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


'''
# Sensor toggling Callback
@app.callback(
        [   # components that will be modified
            Output('enabled-sensors', 'value'),
            Output('cards-container', 'children'),
        ],
        [   # components to listen for to run the callback
            Input('save-checkmarks-button', 'n_clicks_timestamp'),
        ],
        [   # components to get the state of upon callaback
            State('enabled-sensors', 'value'),
        ],
)
def handle_sensor_toggle(button_timestamp, enabledSensorsList):
    if(button_timestamp != None): # Button is clicked
        writeStorageCheckmarks(enabledSensorsList)
        return [dash.no_update, getCardDivs(enabledSensorsList)]
    else: # Button is not clicked
        storageCheckmarks = getStorageCheckmarks()
        return [storageCheckmarks, getCardDivs(storageCheckmarks)]
'''

# callback to update sensor data
@app.callback(
        Output({'type': 'sensor-data', 'index': MATCH}, 'children'),
        Input({'type': 'refresh-button', 'index': MATCH}, 'n_clicks_timestamp'),
        State({'type': 'refresh-button', 'index': MATCH}, 'id'),
)
def handle_refresh_buttons(timestamp, id):
    enabledSensor = id['index']
    return "{} {}".format(Sensor(sensor_names[enabledSensor][1]).getSensorValue(), sensor_names[enabledSensor][2])



@app.callback(
        [
            Output('cards-container', 'children'),
            Output('fields-card', 'children'),
            Output('fields-card', 'style'),
            Output('invalid-selection', 'style'),
            Output('new-card', 'style'),
            Output('field_sensor-name', 'value'),
            Output('field_ip-address', 'value'),
            Output('field_port-number', 'value'),
            Output('field_url-plug', 'value'),
            Output('field_alert', 'value'),
        ],
        [
            Input('new-card-button', 'n_clicks'),
            Input('field_create-card-button', 'n_clicks'),
        ],
        [
            State('cards-container', 'children'),
            State('fields-card', 'children'),
            State('field_sensor-name', 'value'),
            #State('field_units', 'value'),
            State('field_ip-address', 'value'),
            State('field_port-number', 'value'),
            State('field_url-plug', 'value'),
            State('field_alert', 'value'),
        ]
)
def create_new_card(new_card_clicks, create_button_clicks, cardList, fieldsList, sensor_name, ip_address, port, url, alert):
    ctx = dash.callback_context

    curButton = '';

    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]


    print("Create: {} | Add new: {}".format(create_button_clicks, new_card_clicks))

    if(curButton == 'field_create-card-button'):

        if(isValidSensor(url, ip_address, port)):
            print("yes")
            temp = html.Div(className='card',
                    id=sensor_name,
                    children=[
                        html.H4(
                            sensor_name,
                        ),
                        html.H2(str(
                            Sensor(url, port=port, domain=ip_address).getSensorValue()),
                            id={'type': 'sensor-data', 'index': sensor_name},
                        ),
                        html.Button('Refresh',
                            id={'type': 'refresh-button', 'index': sensor_name},
                        ),
                    ]
                )

            tempList = cardList[:-1] + [temp] + [new_sensor_card]
            sensor_names[sensor_name] = (sensor_name, url, '')
            return [tempList, dash.no_update, {'display':'none'}, dash.no_update, {'display':'block'}, '', '', '', '', False]
        else:
            if(len(fieldsList) == 2):
                print("appending")
                return [dash.no_update, fieldsList, dash.no_update, {'display':'block'}, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update]
            return dash.no_update
    elif(curButton == 'new-card-button'):
        print("showing field & hiding new-card")
        return[cardList + [fields_card], dash.no_update, {'display': 'block'}, dash.no_update, {'display': 'none'}, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update]
    else:
        return dash.no_update
        



if __name__ == "__main__":
    app.run_server(debug=True,)
