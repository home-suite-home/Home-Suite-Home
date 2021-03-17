#!/usr/bin/env python
import os
import sys
import json
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

# holds Output parameters as key
# holds return value for Output as value
# NOT actually a dictionary... list of list size two [key, val]
class OutputHolder:
    def __init__(self, inList):
        self.curDictHolder = []

        for item in inList:
            self.curDictHolder.append([item, dash.no_update])

    def getObjList(self):
        return [Output(key[0], key[1]) for key, _ in self.curDictHolder]


    def getReturns(self):
        out = [value for _, value in self.curDictHolder]
        self.__clearHolder()
        return out

    def __clearHolder(self):
        for i in range(len(self.curDictHolder)):
            self.curDictHolder[i][1] = dash.no_update

    def addReturn(self, inkey, invalue):
        for i in range(len(self.curDictHolder)):
            for item in self.curDictHolder[i][0].keys():
                if(item == inkey):
                    self.curDictHolder[i][1] = invalue
                    break

    def printDict(self):
        print('OutputHolder:')
        for key, value in self.curDictHolder:
            print('{}, {}: {}'.format(key[0], key[1], value))


def getCardDivs():
    divList = []

    sensorData = db.getData()
    for sensor in db.getConfigData():
        #print(sensor)
        if(sensor != None):
            sensorName = sensor['name']
            sensorType = sensor['type']

            divList.append(
                html.Div(className='card',
                    id={'type': 'div-card', 'index': '{}`{}'.format(sensorType, sensorName)},
                    children=[
                        html.H4(sensor['name']),
                        html.Div('Type: ' + sensor['type']),
                        html.H2(
                            db.getMostRecentSensorData(sensorName, sensorType),
                            id={'type': 'sensor-data', 'index': '{}`{}'.format(sensorType, sensorName)},
                        ),
                        html.Button('Edit Card', id={'type': 'edit-card-button', 'index': '{}`{}'.format(sensorType, sensorName)}),
                        #html.Button('Edit Card', id='edit-button-{}-{}'.format(sensorType, sensorName)),
                        html.H4(),
                        html.Button('View Graph', id={'type': 'edit-graph-button', 'index': '{}`{}'.format(sensorType, sensorName)}),
                    ]
                )
            )

    divList.append(fields_card)
    divList.append(new_sensor_card)

    return divList


def getTypesDropdownList():
    optionsList = []
    #print("db.getFields('type'):")
    for curType in db.getFields('type'):
        #print(curType)
        optionsList.append({'label': curType, 'value': curType})

    optionsList.append({'label': 'New Type of Sensor', 'value': 'other-type'})

    return optionsList


def fieldsCardToNewCard(cardsList):
    outHolder.addReturn(('cards-container', 'children'), cardsList)
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


db = Database()

new_sensor_card = html.Div(className='card',
                    id='new-card',
                    children=[
                        html.H4(''),
                        html.Button('Add New Sensor', id='new-card-button',),
                    ]
                )

new_card_fields = [
    html.Button('Discard', id='field_discard-button'),
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
            daq.BooleanSwitch(
                id='field_alert',
                className='field_element',
                on=False,
                color='#9ad6aa',
                label='Alerts:',
                labelPosition='top',
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
            html.H4(''),
            html.Div('False', id='isEdit', style={'display':'none'}),
            html.Button('Create', id='field_create-card-button'),
            html.H4('Invalid Selection', style={'color': 'red','display': 'none' }, id='invalid-selection'),
        ],
        style={'display': 'inline-block'}
    ),
]

def populateEditCard(valuesDict):
    field_card_list = [
        html.Button('Discard', id='field_discard-button'),
        html.Div(
            [
                dcc.Input(
                    id='field_sensor-name',
                    className='field_element',
                    autoFocus=True,
                    debounce=True,
                    placeholder='Sensor Name',
                    value=valuesDict['field_sensor-name'],
                ),
                dcc.Dropdown(
                    id='field_types-dropdown',
                    className='field_element',
                    options=getTypesDropdownList(),
                    placeholder='Sensor Type',
                    value=valuesDict['field_types-dropdown'],
                ),
                dcc.Input(
                    id='field_new-type',
                    className='field_element',
                    debounce=True,
                    placeholder='Name of New Type',
                    #value=valuesDict['field_new-type'],
                    style={'display':'none'},
                ),
                dcc.Input(
                    id='field_ip-address',
                    className='field_element',
                    debounce=True,
                    placeholder='IP Address',
                    value=valuesDict['field_ip-address'],
                ),
                dcc.Input(
                    id='field_port-number',
                    className='field_element',
                    debounce=True,
                    placeholder='Port Number (Optional)',
                    value=valuesDict['field_port-number'],
                ),
                dcc.Input(
                    id='field_url-plug',
                    className='field_element',
                    debounce=True,
                    placeholder='URL Plug',
                    value=valuesDict['field_url-plug'],
                ),
                dcc.Input(
                    id='field_units',
                    className='field_element',
                    debounce=True,
                    placeholder='Units (Optional)',
                    value=valuesDict['field_units'],
                ),
                daq.BooleanSwitch(
                    id='field_alert',
                    className='field_element',
                    on=valuesDict['field_alert'],
                    color='#9ad6aa',
                    label='Alerts:',
                    labelPosition='top',
                ),
                dcc.Input(
                    id='field_minimum-bound',
                    className='field_element',
                    debounce=True,
                    placeholder='Minimum bound',
                    value=valuesDict['field_minimum-bound'],
                ),
                dcc.Input(
                    id='field_maximum-bound',
                    className='field_element',
                    debounce=True,
                    placeholder='Maximum bound',
                    value=valuesDict['field_maximum-bound'],
                ),
                html.H4(''),
                html.Div('True', id='isEdit', style={'display':'none'}),
                html.Button('Save', id='field_create-card-button'),
                html.H4('Invalid Selection', style={'color': 'red','display': 'none' }, id='invalid-selection'),
            ],
            style={'display': 'inline-block'}
        ),
    ]

    return field_card_list

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
        children=getCardDivs(),
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
    #({'type': 'card', 'index': MATCH}, 'children'),
    ({'type':'cards-container', 'index': MATCH}, 'children'),
    ({'type':'fields-card', 'index':MATCH}, 'children'),
    ({'type':'fields-card', 'index':MATCH}, 'style'),
    ({'type':'field_sensor-name', 'index': MATCH}, 'value'),
    ({'type':'field_new-type', 'index': MATCH}, 'value'),
    ({'type':'field_new-type', 'index': MATCH}, 'style'),
    ({'type':'field_ip-address', 'index': MATCH}, 'value'),
    ({'type':'field_port-number', 'index': MATCH}, 'value'),
    ({'type':'field_url-plug', 'index': MATCH}, 'value'),
    ({'type':'field_minimum-bound', 'index': MATCH}, 'value'),
    ({'type':'field_maximum-bound', 'index': MATCH}, 'value'),
    ({'type':'field_alert', 'index': MATCH}, 'value'),
    ({'type':'invalid-selection', 'index': MATCH}, 'style'),
    ({'type':'new-card', 'index': MATCH}, 'style'),
    ({'type':'field_types-dropdown', 'index': MATCH}, 'options'),
])

#outHolder.printDict()

@app.callback(
        outHolder.getObjList(),
        [
            Input('new-card-button', 'n_clicks'),
            Input('field_create-card-button', 'n_clicks'),
            Input('field_types-dropdown', 'value'),
            Input('field_discard-button', 'n_clicks'),
            #Input({'type': 'edit-card-button', 'index': MATCH}, 'id'),
        ],
        [
            State({'type':'cards-container', 'index': MATCH}, 'children'),
            State({'type':'fields-card', 'index':MATCH}, 'children'),
            State({'type':'field_sensor-name', 'index': MATCH}, 'value'),
            State({'type':'field_new-type', 'index': MATCH}, 'value'),
            State({'type':'field_units', 'index': MATCH}, 'value'),
            State({'type':'field_ip-address', 'index': MATCH}, 'value'),
            State({'type':'field_port-number', 'index': MATCH}, 'value'),
            State({'type':'field_url-plug', 'index': MATCH}, 'value'),
            State({'type':'field_minimum-bound', 'index': MATCH}, 'value'),
            State({'type':'field_maximum-bound', 'index': MATCH}, 'value'),
            State({'type':'field_alert', 'index': MATCH}, 'value'),
        ]
)
def create_new_card(new_card_clicks, create_button_clicks, sensor_type, discard_button_clicks, #edit_card_button_clicks,
        cardList, fieldsList, sensor_name, new_type, units, ip_address, port, url_plug, min_bound, max_bound, alert):
    print("HELLO")

    ctx = dash.callback_context

    if(port == None or port == ''):
        port = '8080'

    if(units == None):
        units = ''

    curButton = '';


    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]

    print("curButton: ", curButton)

    if(curButton == 'field_create-card-button'):
        print('Stuff: {} {} {}'.format(sensor_type, sensor_name, url_plug))
        if(isValidSensor(sensor_type, url_plug, ip_address, sensor_name, port=port)):
            if(sensor_type == 'other-type'):
                sensor_type = new_type
            db.saveConfigData(sensor_type, sensor_name, 'category', ip_address, port, url_plug, min_bound, max_bound, units, alert)

            fieldsCardToNewCard(cardList)

        else:
            outHolder.addReturn(('invalid-selection', 'style'), {'display':'block', 'color': 'red'})
    elif(curButton == 'new-card-button'):
        outHolder.addReturn(('field_types-dropdown', 'options'), getTypesDropdownList())
        outHolder.addReturn(('fields-card', 'style'), {'display': 'block'}),
        outHolder.addReturn(('new-card', 'style'), {'display': 'none'})
    elif(curButton == 'field_types-dropdown'):
        if(sensor_type == 'other-type'):
            outHolder.addReturn(('field_new-type', 'style'), {'display': 'block'})
    elif(curButton == 'field_discard-button'):
        fieldsCardToNewCard(cardList)
        outHolder.addReturn(('fields-card', 'style'), {'display': 'none'}),
    else:
        outHolder.addReturn(('cards-container', 'children'), getCardDivs())

    outHolder.printDict()
    x = outHolder.getReturns()
    return x


@app.callback(
        Output({'type': 'sensor-data', 'index': MATCH}, 'children'),
        Input('interval-component', 'n_intervals'),
        State({'type': 'sensor-data', 'index': MATCH}, 'id'),
)
def live_data_update(numRefreshes, curId):
    sensorType, sensorName = curId['index'].split('`')
    data = db.getMostRecentSensorData(sensorName, sensorType)

    return data


@app.callback(
        Output({'type': 'div-card', 'index': MATCH}, 'children'),
        Input({'type': 'edit-card-button', 'index': MATCH}, 'n_clicks'),
        State({'type': 'edit-card-button', 'index': MATCH}, 'id')
)
def handle_edit_card(edit_card_button_clicks, curId):

    ctx = dash.callback_context
    curButton = ''

    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]
        try:
            curButton = json.loads(curButton)['type']
        except:
            pass
    
    if(curButton == 'edit-card-button'):
        sensorName, sensorType = curId['index'].split('`')
        config = db.getSensorConfig(sensorType, sensorName)

        fieldsMap = {}
        fieldsMap['field_sensor-name'] = config['name']
        fieldsMap['field_types-dropdown'] = config['type']
        fieldsMap['field_ip-address'] = config['address']
        fieldsMap['field_port-number'] = config['port']
        fieldsMap['field_url-plug'] = config['sub_address']
        fieldsMap['field_units'] = config['units']
        fieldsMap['field_alert'] = config['alerts']
        fieldsMap['field_minimum-bound'] = config['min_threshold']
        fieldsMap['field_maximum-bound'] = config['max_threshold']

        print('getSensorConfig({}, {}) = {}'.format(sensorType, sensorName, config))


        x = populateEditCard(fieldsMap)
        #print(x)
        return x
    else:
        return dash.no_update



if __name__ == "__main__":
    ip_address = check_output(["hostname", "-I"]).decode("utf-8").split(" ")[0]
    print("IP Address: ", ip_address)
    port = 8050
    print("Port: ", port)
    app.run_server(debug=True, host=ip_address, port=port)
