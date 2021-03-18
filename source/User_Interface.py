#!/usr/bin/env python
import os
import sys
import json
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
from Email_Component import Email_Component
from HTTP_Component.Sensors import Sensor
from UI_Utils import *
from subprocess import check_output
from collections import OrderedDict
from Server_Component.Database import Database

SECONDS_PER_REFRESH = 30
NU = dash.no_update

## holds Output parameters as key
# holds return value for Output as value
# NOT actually a dictionary... list of list size two [key, val]
#class OutputHolder:
#    def __init__(self, inList):
#        self.curDictHolder = []
#
#        for item in inList:
#            self.curDictHolder.append([item, dash.no_update])
#
#    def getObjList(self):
#        return [Output(key[0], key[1]) for key, _ in self.curDictHolder]
#
#
#    def getReturns(self):
#        out = [value for _, value in self.curDictHolder]
#        self.__clearHolder()
#        return out
#
#    def __clearHolder(self):
#        for i in range(len(self.curDictHolder)):
#            self.curDictHolder[i][1] = dash.no_update
#
#    def addReturn(self, inkey, invalue):
#        for i in range(len(self.curDictHolder)):
#            if(type(self.curDictHolder[i][0][0]) == dict):
#                for item in self.curDictHolder[i][0][0].keys():
#                    if(item == inkey):
#                        self.curDictHolder[i][1] = invalue
#                        break
#            else:
#                print(self.curDictHolder[i])
#                print('test: ',self.curDictHolder[i][0][1] ,inkey)
#                if(self.curDictHolder[i][0][0] == inkey[0] and
#                        self.curDictHolder[i][0][1] ==inkey[1]):
#                    print('adding ',self.curDictHolder[i][0][0],invalue)
#                    self.curDictHolder.insert(i, [self.curDictHolder[i][0][0],invalue])
#                    print(self.curDictHolder[i][1], invalue)
#
#    def printDict(self):
#        print('OutputHolder:')
#        for key, value in self.curDictHolder:
#            print('{}, {}: {}'.format(key[0], key[1], value))


def getCardDivs(isField=False, isEdit=False):
    divList = []

    sensorData = db.getData()
    for sensor in db.getConfigData():
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
                        html.H4(),
                        html.Button('View Graph', id={'type': 'graph-card-button', 'index': '{}`{}'.format(sensorType, sensorName)}),
                    ]
                )
            )

    tempEditCard, tempFieldsCard, tempNewCard = getFieldsAndNewAndEditCards(isField=isField, isEdit=isEdit)
    divList.append(tempEditCard)
    divList.append(tempFieldsCard)
    divList.append(tempNewCard)

    return divList


def getTypesDropdownList():
    optionsList = []
    print("db.getFields('type'):")
    for curType in db.getFields('type'):
        print(curType)
        optionsList.append({'label': curType, 'value': curType})

    optionsList.append({'label': 'New Type of Sensor', 'value': 'other-type'})

    return optionsList


def getFieldsAndNewAndEditCards(isField=False, isEdit=False):
    if(isField):
        displayFields = 'inline-block'
        displayNew = 'none'
    else:
        displayFields = 'none'
        displayNew = 'inline-block'
    if(isEdit):
        displayEdit = 'inline-block'
    else:
        displayEdit = 'none'

    temp_edits_card = html.Div(className='card',
                        id='edits-card',
                        children=edit_card_fields,
                        style={'display': displayEdit},
                    )

    temp_fields_card = html.Div(className='card',
                        id='fields-card',
                        children=new_card_fields,
                        style={'display': displayFields},
                    )
    
    temp_new_sensor_card = html.Div(className='card',
                        id='new-card',
                        children=[
                            html.H4(''),
                            html.Button('Add New Sensor', id='new-card-button',),
                        ],
                        style={'display': displayNew}
                    )

    return temp_edits_card, temp_fields_card, temp_new_sensor_card


def populateEditCard(valuesDict):
    edit_card_list = [
        html.Button('Discard', id='edit_discard-button'),
        html.Div(
            [
                dcc.Input(
                    id='edit_sensor-name',
                    className='field_element',
                    autoFocus=True,
                    debounce=True,
                    placeholder='Sensor Name',
                    value=valuesDict['edit_sensor-name'],
                ),
                dcc.Dropdown(
                    id='edit_types-dropdown',
                    className='field_element',
                    options=getTypesDropdownList(),
                    placeholder='Sensor Type',
                    value=valuesDict['edit_types-dropdown'],
                ),
                dcc.Input(
                    id='edit_new-type',
                    className='field_element',
                    debounce=True,
                    placeholder='Name of New Type',
                    style={'display':'none'},
                ),
                dcc.Input(
                    id='edit_ip-address',
                    className='field_element',
                    debounce=True,
                    placeholder='IP Address',
                    value=valuesDict['edit_ip-address'],
                ),
                dcc.Input(
                    id='edit_port-number',
                    className='field_element',
                    debounce=True,
                    placeholder='Port Number (Optional)',
                    value=valuesDict['edit_port-number'],
                ),
                dcc.Input(
                    id='edit_url-plug',
                    className='field_element',
                    debounce=True,
                    placeholder='URL Plug',
                    value=valuesDict['edit_url-plug'],
                ),
                dcc.Input(
                    id='edit_units',
                    className='field_element',
                    debounce=True,
                    placeholder='Units (Optional)',
                    value=valuesDict['edit_units'],
                ),
                daq.BooleanSwitch(
                    id='edit_alert',
                    className='field_element',
                    on=valuesDict['edit_alert'],
                    color='#9ad6aa',
                    label='Alerts:',
                    labelPosition='top',
                ),
                dcc.Input(
                    id='edit_minimum-bound',
                    className='field_element',
                    debounce=True,
                    placeholder='Minimum bound',
                    value=valuesDict['edit_minimum-bound'],
                ),
                dcc.Input(
                    id='edit_maximum-bound',
                    className='field_element',
                    debounce=True,
                    placeholder='Maximum bound',
                    value=valuesDict['edit_maximum-bound'],
                ),
                html.H4(''),
                html.Button('Save', id='edit_save-card-button'),
                html.H4('Invalid Selection', style={'color': 'red','display': 'none' }, id='edit_invalid-selection'),
            ],
            style={'display': 'inline-block'}
        ),
    ]

    return edit_card_list


db = Database()

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

edit_card_fields = [
    html.Button('Discard', id='edit_discard-button'),
    html.Div(
        [
            dcc.Input(
                id='edit_sensor-name',
                className='edit_element',
                autoFocus=True,
                debounce=True,
                placeholder='Sensor Name',
            ),
            dcc.Dropdown(
                id='edit_types-dropdown',
                className='edit_element',
                options=getTypesDropdownList(),
                placeholder='Sensor Type',
            ),
            dcc.Input(
                id='edit_new-type',
                className='edit_element',
                debounce=True,
                placeholder='Name of New Type',
                style={'display':'none'},
            ),
            dcc.Input(
                id='edit_ip-address',
                className='edit_element',
                debounce=True,
                placeholder='IP Address',
            ),
            dcc.Input(
                id='edit_port-number',
                className='edit_element',
                debounce=True,
                placeholder='Port Number (Optional)',
            ),
            dcc.Input(
                id='edit_url-plug',
                className='edit_element',
                debounce=True,
                placeholder='URL Plug',
            ),
            dcc.Input(
                id='edit_units',
                className='edit_element',
                debounce=True,
                placeholder='Units (Optional)',
            ),
            dcc.Input(
                id='edit_minimum-bound',
                className='edit_element',
                debounce=True,
                placeholder='Minimum bound',
            ),
            dcc.Input(
                id='edit_maximum-bound',
                className='edit_element',
                debounce=True,
                placeholder='Maximum bound',
            ),
            daq.BooleanSwitch(
                id='edit_alert',
                className='edit_element',
                on=False,
                color='#9ad6aa',
                label='Alerts:',
                labelPosition='top',
            ),
            html.H4(''),
            html.Button('save', id='edit_save-card-button'),
            html.H4('Invalid Selection', style={'color': 'red','display': 'none' }, id='edit_invalid-selection'),
        ],
        style={'display': 'inline-block'}
    ),
]

new_sensor_card = html.Div(className='card',
                    id='new-card',
                    children=[
                        html.H4(''),
                        html.Button('Add New Sensor', id='new-card-button',),
                    ]
                )

fields_card = html.Div(className='card',
                    id='fields-card',
                    children=new_card_fields,
                    style={'display': 'none'},
                )

edits_card = html.Div(className='card',
                    id='edits-card',
                    children=edit_card_fields,
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
    html.Div(id='createCardMessenger',style={'display':'none'}),
    html.Div(id='editCardMessenger', style={'display':'none'}),
    html.Div(id="cards-container",
        style={
            'width': '100%',
            'height': '100%',
            'display': 'grid',
            'align-content': 'start',
            'grid-template-columns': 'repeat(auto-fill, 230px)',

        },
        children=[
            edits_card, 
            fields_card, 
            new_sensor_card
        ]
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


# Editor of cards-container.
# Anything that wants to change cards-container has to send a 'messenger' to this callback.
@app.callback(
        Output('cards-container','children'),
        [
            Input('new-card-button', 'n_clicks'),
            Input('createCardMessenger', 'children'),
            Input('editCardMessenger', 'children'),
            Input('field_discard-button', 'n_clicks'),
            Input('edit_discard-button', 'n_clicks'),
        ]
)
def set_cards_container(sensor_button, createCardMessenger, editCardMessenger, field_discard_button,
        edit_discard_button):
    ctx = dash.callback_context
    curButton = '';
    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]
    print('(set_cards_container) curButton: ', curButton)
    
    if(curButton == 'new-card-button'):
        return getCardDivs(isField=True)
    elif(curButton == 'createCardMessenger'):
        return getCardDivs()
    elif(curButton == 'editCardMessenger'):
        print('is editing!')
        #return getCardDivs(isEdit=True)
        return getCardDivs()
    elif(curButton == 'field_discard-button'):
        return getCardDivs()
    elif(curButton =='edit_discard-button'):
        if(edit_discard_button is not None):
            return getCardDivs()
        else:
            return NU
    else:
        return getCardDivs()


@app.callback(
        [
            Output('createCardMessenger', 'children'),
            Output('invalid-selection', 'style'),
            Output('field_new-type', 'style'),
        ],
        [

            Input('field_create-card-button', 'n_clicks'),
            Input('field_types-dropdown', 'value'),
        ],
        [
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
def create_new_card(create_button, sensor_type,
        sensor_name, new_type, units, ip_address, port, url_plug, min_bound, max_bound, alert,):


    if(port == None or port == ''):
        port = '8080'
    if(alert == None):
        alert = False

    if(units == None):
        units = ''

    ctx = dash.callback_context
    curButton = '';

    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]

    print('(create_new_card) curButton: ', curButton)

    if(curButton == 'field_create-card-button'):
        if(isValidSensor(sensor_type, url_plug, ip_address, sensor_name, port=port)):
            if(sensor_type == 'other-type'):
                sensor_type = new_type
            db.saveConfigData(sensor_type, sensor_name, 'category', ip_address, port, url_plug, min_bound, max_bound, units, alert)

            return [html.Div(), NU, NU]

        else:
            return [NU, {'display':'block', 'color': 'red'}, NU]
    elif(curButton == 'field_types-dropdown'):
        if(sensor_type == 'other-type'):
            return [NU, NU, {'display':'block'}]

    return NU


@app.callback(
        Output({'type': 'div-card', 'index': MATCH}, 'children'),
        Input({'type': 'edit-card-button', 'index': MATCH}, 'n_clicks'),
        State({'type': 'edit-card-button', 'index': MATCH}, 'id'),

)
def handle_edit_button(edit_button, curId):
    ctx = dash.callback_context
    curButton = '';
    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]
        try:
            curButton = json.loads(curButton)['type']
        except:
            pass


    print('(handle_edit_button) curButton: ', curButton)

    if(curButton == 'edit-card-button'):
        sensorName, sensorType = curId['index'].split('`')
        config = db.getSensorConfig(sensorType, sensorName)

        fieldsMap = {}
        fieldsMap['edit_sensor-name'] = config['name']
        fieldsMap['edit_types-dropdown'] = config['type']
        fieldsMap['edit_ip-address'] = config['address']
        fieldsMap['edit_port-number'] = config['port']
        fieldsMap['edit_url-plug'] = config['sub_address']
        fieldsMap['edit_units'] = config['units']
        fieldsMap['edit_alert'] = config['alerts']
        fieldsMap['edit_minimum-bound'] = config['min_threshold']
        fieldsMap['edit_maximum-bound'] = config['max_threshold']

        print('getSensorConfig({}, {}) = {}'.format(sensorType, sensorName, config))

        return populateEditCard(fieldsMap)
    else:
        return NU


@app.callback(
        [
            Output('editCardMessenger','children'),
            Output('edit_invalid-selection', 'style'),
            Output('edit_new-type', 'style'),
        ],
        [
            Input('edit_save-card-button', 'n_clicks'),
            Input('edit_types-dropdown', 'value'),
        ],
        [
            State('edit_sensor-name', 'value'),
            State('edit_new-type', 'value'),
            State('edit_units', 'value'),
            State('edit_ip-address', 'value'),
            State('edit_port-number', 'value'),
            State('edit_url-plug', 'value'),
            State('edit_minimum-bound', 'value'),
            State('edit_maximum-bound', 'value'),
            State('edit_alert', 'value'),
        ]
)
def save_edit_card(save_button, sensor_type,
        sensor_name, new_type, units, ip_address, port, url_plug, min_bound, max_bound, alert,):
    ctx = dash.callback_context
    curButton = '';
    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]
    print('(save_edit_card) curButton: ', curButton)

    if(curButton == 'edit_save-card-button'):
        if(isValidSensor(sensor_type, url_plug, ip_address, sensor_name, port=port)):
            if(sensor_type == 'other-type'):
                sensor_type = new_type
            #db.deleteConfigData(sensor_name, sensor_type)
            db.saveConfigData(sensor_type, sensor_name, 'category', ip_address, port, url_plug, min_bound, max_bound, units, alert)

            return [html.Div(), NU, NU]

        else:
            return [NU, {'display':'block', 'color': 'red'}, NU]
    elif(curButton == 'edit_types-dropdown'):
        print(sensor_type)
        if(sensor_type == 'other-type'):
            print('displaying new type')
            return [NU, NU, {'display':'block'}]

    return NU

@app.callback(
        Output({'type': 'sensor-data', 'index': MATCH}, 'children'),
        Input('interval-component', 'n_intervals'),
        State({'type': 'sensor-data', 'index': MATCH}, 'id'),
)
def live_data_update(numRefreshes, curId):
    sensorType, sensorName = curId['index'].split('`')
    data = db.getMostRecentSensorData(sensorName, sensorType)

    return data


if __name__ == "__main__":
    ip_address = check_output(["hostname", "-I"]).decode("utf-8").split(" ")[0]
    print("IP Address: ", ip_address)
    port = 8050
    print("Port: ", port)
    app.run_server(debug=True, host=ip_address, port=port)