#!/usr/bin/env python
import os
import sys
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate
from Email_Component import Email_Component
from HTTP_Component.Sensors import Sensor
from UI_Utils import *
from subprocess import check_output
from collections import OrderedDict
from Server_Component.Database import Database

SECONDS_PER_REFRESH = 30

class OutputHolder:
    def __init__(self, inList):
        self.curDictHolder = OrderedDict()

        for item in inList:
            self.curDictHolder[item] = dash.no_update

    def getObjList(self):
        return [Output(key[0], key[1]) for key, _ in self.curDictHolder.items()]

    def getReturns(self):
        out = [value for _, value in self.curDictHolder.items()]
        self.__clearHolder()
        return out

    def __clearHolder(self):
        for key, _ in self.curDictHolder.items():
            self.curDictHolder[key] = dash.no_update

    def addReturn(self, key, value):
        self.curDictHolder[key] = value

    def printDict(self):
        print(self.curDictHolder)


def getCardDivs():
    divList = []

    sensorData = db.getData()
    for sensor in db.getConfigData():
        print(sensor)
        if(sensor != None):
            divList.append(
                html.Div(className='card',
                    children=[
                        html.H4(sensor['name']),
                        html.Div('Type: ' + sensor['type']),
                        html.H2(
                            db.getMostRecentSensorData(sensor['name'], sensor['type']),
                            id={'type': 'sensor-data', 'index': '{}-{}'.format(sensor['type'], sensor['name'])},
                        ),
                    ]
                )
            )

    divList.append(fields_card)
    divList.append(new_sensor_card)

    return divList


def getTypesDropdownList():
    optionsList = []
    for curType in db.getFields('type'):
        optionsList.append({'label': curType, 'value': curType})

    optionsList.append({'label': 'New Type of Sensor', 'value': 'other-type'})

    return optionsList


db = Database()

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
                className='field_element',
                autoFocus=True,
                debounce=True,
                placeholder='Sensor Name',
            ),
            dcc.Dropdown(
                id='field_types-dropdown',
                className='field_element',
                options=getTypesDropdownList(),
                placeholder='Sensor Type',
            ),
            dcc.Input(
                id='field_new-type',
                className='field_element',
                debounce=True,
                placeholder='Name of New Type',
                style={'display':'none'},
            ),
            dcc.Input(
                id='field_ip-address',
                className='field_element',
                debounce=True,
                placeholder='IP Address',
            ),
            dcc.Input(
                id='field_port-number',
                className='field_element',
                debounce=True,
                placeholder='Port Number (Optional)',
            ),
            dcc.Input(
                id='field_url-plug',
                className='field_element',
                debounce=True,
                placeholder='URL Plug',
            ),
            dcc.Input(
                id='field_units',
                className='field_element',
                debounce=True,
                placeholder='Units (Optional)',
            ),
            dcc.Input(
                id='field_minimum-bound',
                className='field_element',
                debounce=True,
                placeholder='Minimum bound',
            ),
            dcc.Input(
                id='field_maximum-bound',
                className='field_element',
                debounce=True,
                placeholder='Maximum bound',
            ),
            daq.BooleanSwitch(
                id='field_alert',
                className='field_element',
                on=False,
                color='#9ad6aa',
                label='Alerts:',
                labelPosition='top',
            ),
            html.H4(''),
            html.Button('Create', id='field_create-card-button'),
            html.H4('Invalid Selection', style={'color': 'red','display': 'none' }, id='invalid-selection'),
        ],
        style={'display': 'inline-block'}
    ),
]

fields_card = html.Div(className='card',
                    id='fields-card',
                    children=new_card_fields,
                    style={'display': 'none'},
                )


colors = {"background": "343434"}
app = dash.Dash(__name__, suppress_callback_exceptions=True)


mainDivChildren = [
    dcc.Interval(
        id='interval-component',
        interval=SECONDS_PER_REFRESH*1000, # in ms
        n_intervals=0,
    ),
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
                ],
            ),
        ],
    ),
    html.Div(id="cards-container",
        style={
            'width': '100%',
            'height': '100%',
            'display': 'grid',
            'align-content': 'start',
            'grid-template-columns': 'repeat(auto-fill, 230px)',

        },
        children=[fields_card, new_sensor_card,]
    ),
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


outHolder = OutputHolder([
    ('cards-container', 'children'),
    ('fields-card', 'children'),
    ('fields-card', 'style'),
    ('invalid-selection', 'style'),
    ('new-card', 'style'),
    ('field_sensor-name', 'value'),
    ('field_new-type', 'style'),
    ('field_new-type', 'value'),
    ('field_minimum-bound', 'value'),
    ('field_maximum-bound', 'value'),
    ('field_ip-address', 'value'),
    ('field_port-number', 'value'),
    ('field_url-plug', 'value'),
    ('field_alert', 'value'),
])

@app.callback(
        outHolder.getObjList(),
        [
            Input('new-card-button', 'n_clicks'),
            Input('field_create-card-button', 'n_clicks'),
            Input('field_types-dropdown', 'value'),
        ],
        [
            State('cards-container', 'children'),
            State('fields-card', 'children'),
            State('field_sensor-name', 'value'),
            State('field_new-type', 'value'),
            State('field_units', 'value'),
            State('field_ip-address', 'value'),
            State('field_port-number', 'value'),
            State('field_url-plug', 'value'),
            State('field_minimum-bound', 'value'),
            State('field_maximum-bound', 'value'),
            State('field_alert', 'value'),
        ]
)
def create_new_card(new_card_clicks, create_button_clicks, sensor_type, 
        cardList, fieldsList, sensor_name, new_type, units, ip_address, port, url_plug, min_bound, max_bound, alert):

    ctx = dash.callback_context

    if(port == None or port == ''):
        port = '8080'

    if(units == None):
        units = ''

    curButton = '';


    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]

    if(curButton == 'field_create-card-button'):
        if(isValidSensor(sensor_type, url_plug, ip_address, sensor_name, port=port)):
            if(sensor_type == 'other-type'):
                sensor_type = new_type
            db.saveConfigData(sensor_type, sensor_name, 'category', ip_address, port, url_plug, min_bound, max_bound, units, alert)

            
            outHolder.addReturn(('cards-container', 'children'), getCardDivs())
            outHolder.addReturn(('invalid-selection', 'style'), {'display': 'none'})

            # clear the fields
            outHolder.addReturn(('field_sensor-name', 'value'), '')
            outHolder.addReturn(('field_new-type', 'value'), '')
            outHolder.addReturn(('field_new-type', 'style'), {'display': 'none'})
            outHolder.addReturn(('field_ip-address', 'value'), '')
            outHolder.addReturn(('field_port-number', 'value'), '')
            outHolder.addReturn(('field_url-plug', 'value'), '')
            outHolder.addReturn(('field_alert', 'value'), False)

            outHolder.addReturn(('new-card', 'style'), {'display': 'block'})

        else:
            outHolder.addReturn(('invalid-selection', 'style'), {'display':'block', 'color': 'red'})
    elif(curButton == 'new-card-button'):
        outHolder.addReturn(('fields-card', 'style'), {'display': 'block'}),
        outHolder.addReturn(('new-card', 'style'), {'display': 'none'})
    elif(curButton == 'field_types-dropdown'):
        if(sensor_type == 'other-type'):
            outHolder.addReturn(('field_new-type', 'style'), {'display': 'block'})
    else:
        outHolder.addReturn(('cards-container', 'children'), getCardDivs())

    return outHolder.getReturns()


@app.callback(
        Output({'type': 'sensor-data', 'index': MATCH}, 'children'),
        Input('interval-component', 'n_intervals'),
        State({'type': 'sensor-data', 'index': MATCH}, 'id'),
)
def live_data_update(numRefreshes, curId):
    sensorType, sensorName = curId['index'].split('-')
    data = db.getMostRecentSensorData(sensorName, sensorType)

    return data


if __name__ == "__main__":
    ip_address = check_output(["hostname", "-I"]).decode("utf-8").split(" ")[0]
    print("IP Address: ", ip_address)
    port = 8050
    print("Port: ", port)
    app.run_server(debug=True, host=ip_address, port=port)
