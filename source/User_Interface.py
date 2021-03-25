#!/usr/bin/env python
import os
import sys
import json
import dash
import urllib
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
from Email_Component import Email_Component
from AnalyticsComponent import LineGraph
from HTTP_Component.Sensors import Sensor
from UI_Utils import *
from subprocess import check_output
from collections import OrderedDict
from Server_Component.Database import Database
from settings import Settings
from conversions import Units


SECONDS_PER_REFRESH = 30
NU = dash.no_update

settings = Settings()

def getCardDivs(isField=False, isEdit=False):
    divList = []

    sensorData = db.getData()
    for sensor in db.getConfigData():
        if(sensor != None):
            sensorName = sensor['name']
            sensorType = sensor['type']

            curUnits = Units(sensorType, sensor['units'])
            cardData = curUnits.convert_to_string(db.getMostRecentSensorData(sensorName, sensorType))
            print(cardData)

            divList.append(
                html.Div(className='card',
                    id={'type': 'div-card', 'index': '{}`{}'.format(sensorType, sensorName)},
                    children=[
                        html.H4(sensor['name']),
                        html.Div('Type: ' + sensor['type']),
                        html.H2(
                            cardData,
                            id={'type': 'sensor-data', 'index': '{}`{}'.format(sensorType, sensorName)},
                        ),
                        html.Button('Edit Card', id={'type': 'edit-card-button', 'index': '{}`{}'.format(sensorType, sensorName)}),
                        html.H4(),
                        dcc.Link(
                            html.Button('View Graph', id={'type': 'graph-card-button', 'index': '{}`{}'.format(sensorType, sensorName)}),
                            href='/analytics/{}'.format(urllib.parse.urlencode(
                                {'name': sensorName, 'type': sensorType}))
                        )
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
    #print("db.getFields('type'):")
    for curType in db.getFields('type'):
        #print(curType)
        optionsList.append({'label': curType, 'value': curType})

    optionsList.append({'label': 'New Type of Sensor', 'value': 'other-type'})

    return optionsList


def getUsersDropdownLists(getOptions=False, getValue=False):
    optionsDictList = []
    optionsList = []

    print('GETTING STUFF')

    if(getOptions and getValue):
        for curUser in db.getAllUsers():
            optionsDictList.append({'label': curUser['email'], 'value': curUser['email']})
            optionsList.append(curUser['email'])
        return optionsDictList, optionsList
    elif(getOptions):
        for curUser in db.getAllUsers():
            optionsDictList.append({'label': curUser['email'], 'value': curUser['email']})
        return optionsDictList
    elif(getValue):
        for curUser in db.getAllUsers():
            optionsList.append(curUser['email'])
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


def populateEditCard(valuesDict, curId):
    print("(populateEditCard) " + str(curId['index']))
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
                #dcc.Dropdown(
                #    id='edit_types-dropdown',
                #    className='field_element',
                #    options=getTypesDropdownList(),
                #    placeholder='Sensor Type',
                #    value=valuesDict['edit_types-dropdown'],
                #),
                #dcc.Input(
                #    id='edit_new-type',
                #    className='field_element',
                #    debounce=True,
                #    placeholder='Name of New Type',
                #    style={'display':'none'},
                #),
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
                html.H4(''),
                html.Div(curId['index'], id='edit_name-passer', style={'display':'none'}),
                html.Button('DELETE', id='edit_delete-button'),
                html.H4('Invalid Selection', style={'color': 'red','display': 'none' }, id='edit_invalid-selection'),
            ],
            style={'display': 'inline-block'}
        ),
    ]

    return edit_card_list


def getAnalyticsPage(sensorType, sensorName):
    analyticsPage = [
        html.Div(
            children=[
                html.H1(children="Analytics"),
                dcc.Link('Homepage', href='/'),
                html.Br(),
                html.Div(
                    id='graph_holder',
                    children=[
                        dcc.Graph(
                            id={'type':'graph', 'index':'{}-{}'.format(sensorType, sensorName)},
                            figure=LineGraph.with_buttons(sensorType, sensorName),
                            style={'display':'block'},
                        )
                    ],
                )
            ],
            style={'display':'block', 'textAlign':'center'}
        )
    ]

    return analyticsPage


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
            #dcc.Dropdown(
            #    id='edit_types-dropdown',
            #    className='edit_element',
            #    options=getTypesDropdownList(),
            #    placeholder='Sensor Type',
            #),
            #dcc.Input(
            #    id='edit_new-type',
            #    className='edit_element',
            #    debounce=True,
            #    placeholder='Name of New Type',
            #    style={'display':'none'},
            #),
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
            html.H4(''),
            html.Div('default', id='edit_name-passer', style={'display':'none'}),
            html.Button('DELETE', id='edit_delete-button'),
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


mainPage = [
    dcc.Location(id='url', refresh=False),
    dcc.Interval(
        id='interval-component',
        interval=SECONDS_PER_REFRESH*1000, # in ms
        n_intervals=0,
    ),
    html.Div(id='page-content'),
]

mainDivChildren =[
    html.Div(
        id="title",
        children=[
            html.H1(children="Home Sensor Suite"),
            dcc.Link('Settings', href='/settings'),
        ],
        style={"textAlign": "center"},
    ),
    html.Div(id='createCardMessenger',style={'display':'none'}),
    html.Div(id='editCardMessenger', style={'display':'none'}),
    html.Div(id='deleteCardMessenger', style={'display':'none'}),
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


dropdownOptions, dropdownValue = getUsersDropdownLists(getOptions=True, getValue=True)

settingsPage = [
    html.Div(children=[
        html.H1(children="Settings"),
        dcc.Link('Homepage', href='/'),
        html.Div(
            id="major_container1",
            style={
                'width': '100%',
                'height': '100%',
                'display':'grid',
                'grid-template-columns': '33.33% 33.33% 33.33%',
            },
            children=[
                html.Div(id='dump', style={'display':'none'}),
                html.Div(
                    id="retrieve-email",
                    className="settings_column",
                    children=[
                        html.H3(children='RaspberryPi Email'),
                        dcc.Input(
                            id="pi-email",
                            placeholder="Enter a New Email for the RaspberryPi",
                            className="settings_input",
                            type="email",
                            value="",
                            debounce=True,
                        ),
                        dcc.Input(
                            id='pi-password',
                            placeholder="Enter Password for Pi's Email",
                            type="password",
                            className="settings_input",
                            value="",
                            debounce=True,
                        ),
                        html.Button("Submit", id="pi-button",),
                    ],
                ),
                html.Div(
                    id='user-emails',
                    className="settings_column",
                    children=[
                        html.H3('User Emails'),
                        dcc.Input(
                            id="user-email-input",
                            placeholder="Enter a User's Email",
                            type='email',
                            className='settings_input',
                            value='',
                            debounce=True,
                            style={
                                'border-width': 'thin',
                                'width': '100%',
                                'height': '40px',
                            }
                        ),
                        html.Button(
                            children='Add',
                            id='new-user-button',
                        ),
                        html.Br(),
                        html.Br(),
                        html.Div('Enable Alerts for Emails:'),
                        dcc.Dropdown(
                            id='users-dropdown',
                            #options=getUsersDropdownLists(getOptions=True),
                            #value=getUsersDropdownLists(getValue=True),
                            options=dropdownOptions,
                            value=dropdownValue,
                            className='settings_input',
                            multi=True,
                            clearable=False,
                            style={'display':'inline-block', 'height':'auto'}
                        ),
                        html.Br(),
                    ]
                ),
                html.Div(
                    id='other-settings',
                    className="settings_column",
                    children=[
                        html.H3('Other Settings'),
                        html.Div('Disable ALL Email Notifications:'),
                        daq.BooleanSwitch(
                            id='global-switch',
                            on=settings.get_bool_setting('alerts', 'silence_alerts'),
                            color='#9ad6aa',
                            labelPosition='top',
                        ),
                        html.Br(),
                        html.Div('Cooldown Between Email Notifications in Minutes:'),
                        dcc.Input(
                            id='email-rate-limit',
                            type='number',
                            value=settings.get_int_setting('alerts', 'rate_limit'),
                        ),
                        html.Br(),
                        html.Br(),
                        html.Div("Sensor's Polling Rate in Seconds:"),
                        dcc.Input(
                            id='poll-rate',
                            type='number',
                            value=settings.get_int_setting('sensors', 'poll_rate'),
                        )
                    ]
                )
            ],
        ),
    ],
    style={'textAlign':'center'},
    )
]


analyticsPage = [
    html.H1(children="Analytics"),
    dcc.Link('Homepage', href='/'),
    html.Div(
        id='graph_holder',
        children=[
            dcc.Graph(
                id='graph',
                style={'display':'inline-block'}
            )
        ],
        style={'display':'inline-block', 'textAlign':'center'}
    )
]


errorPage = [
    html.H1("ERROR")
]


app.layout = html.Div(
        style={"backgroundColor": colors["background"]},
        children=mainPage
)


@app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname'),
)
def display_page(pathname):
    pathname_split = pathname.split('/')

    if(pathname == '/'):
        return mainDivChildren
    if(pathname == '/settings'):
        return settingsPage
    if(len(pathname_split) == 3):
        pair_dict = urllib.parse.parse_qs(pathname_split[-1])
        sensorName = pair_dict['name'][0]
        sensorType = pair_dict['type'][0]
        print("NAME-TYPE: ", sensorName, sensorType)

        if(db.getSensorConfig(sensorName, sensorType)):
            return getAnalyticsPage(sensorType, sensorName)
        else:
            return errorPage
    else:
        return errorPage


# Email Entry Callback
@app.callback(
        [
            Output("pi-email", "value"),
            Output('pi-password', 'value')
        ],
        Input("pi-button", "n_clicks_timestamp"),
        [
            State("pi-email", "value"),
            State('pi-password', 'value'),
        ],
)
def handle_email(button_timestamp, email, password):
    if(button_timestamp != None):
        #try:
        #    print("Sending a test email to " + email)
        #    confirmation = Email_Component(email)

        #    print(confirmation.confirmation_email())
        #except:
        #    print("Error: Unable to send a test email to " + email)

        #return ""
        db.saveCredentials(email, password)
        print("yo")
        return ['','']
    else:
        return dash.no_update


@app.callback(
        [
            Output('users-dropdown', 'options'),
            Output('users-dropdown', 'value'),
            Output('user-email-input', 'value'),
        ],
        [
            Input('new-user-button', 'n_clicks'),
            Input('users-dropdown', 'value'),
        ],
        [
            State('user-email-input', 'value'),
        ]
)
def handle_users(add_button, dropdown_value, email):
    ctx = dash.callback_context
    curButton = '';
    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]
    #print('(handle_users) curButton: ', curButton)

    if(curButton == 'users-dropdown'):
        dbValue = getUsersDropdownLists(getValue=True)

        dbValue = set(dbValue)
        dropdown_value = set(dropdown_value)

        if(dropdown_value != dbValue):
            toDelete = dbValue.difference(dropdown_value)

            for email in toDelete:
                print('deleting email: ', email)
                db.deleteUser(email)

        dbOptions, dbValue = getUsersDropdownLists(getOptions=True, getValue=True)
        return [dbOptions, dbValue, NU]
    elif(curButton == 'new-user-button' and add_button != None):
        db.saveUser(None, email)
        dbOptions, dbValue = getUsersDropdownLists(getOptions=True, getValue=True)
        return [dbOptions, dbValue, '']
    else:
        dbOptions, dbValue = getUsersDropdownLists(getOptions=True, getValue=True)
        return [dbOptions, dbValue, NU]

    return NU

@app.callback(
        [
            Output('global-switch', 'on'),
            Output('email-rate-limit', 'value'),
            Output('poll-rate', 'value'),
        ],
        [
            Input('global-switch', 'on'),
            Input('email-rate-limit', 'value'),
            Input('poll-rate', 'value'),
        ],
)
def other_settings(switch ,rate_limit, polling):
    ctx = dash.callback_context
    curButton = '';
    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]
    print('(other_settings) curButton: ', curButton)

    if(curButton == 'global-switch'):
        settings.set_setting('alerts', 'silence_alerts', str(switch))
        return [switch, NU, NU]
    elif(curButton == 'email-rate-limit'):
        settings.set_setting('alerts', 'rate_limit', str(rate_limit))
        return [NU, rate_limit, NU]
    elif(curButton == 'poll-rate'):
        settings.set_setting('sensors', 'poll_rate', str(polling))
        return [NU, NU, polling]
    else:
        switch = settings.get_bool_setting('alerts', 'silence_alerts')
        rate_limit = settings.get_setting('alerts', 'rate_limit')
        polling = settings.get_setting('sensors', 'poll_rate')

        return [switch, rate_limit, polling]


    return NU



# Editor of cards-container.
# Anything that wants to change cards-container has to send a 'messenger' to this callback.
@app.callback(
        Output('cards-container','children'),
        [
            Input('new-card-button', 'n_clicks'),
            Input('createCardMessenger', 'children'),
            Input('editCardMessenger', 'children'),
            Input('deleteCardMessenger', 'children'),
            Input('field_discard-button', 'n_clicks'),
            Input('edit_discard-button', 'n_clicks'),
        ]
)
def set_cards_container(sensor_button, createCardMessenger, editCardMessenger,
        deleteCardMessenger,
        field_discard_button,edit_discard_button):
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
    elif(curButton == 'deleteCardMessenger'):
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
            State('field_alert', 'on'),
        ]
)
def create_new_card(create_button, sensor_type,
        sensor_name, new_type, units, ip_address, port, url_plug, min_bound, max_bound, alert,):

    #print("Alert: " + str(alert))

    if(port == None or port == ''):
        port = '8080'

    if(units == None):
        units = ''

    try:
        min_bound = float(min_bound)
    except:
        pass
    try:
        max_bound = float(max_bound)
    except:
        pass

    ctx = dash.callback_context
    curButton = '';

    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]

    print('(create_new_card) curButton: ', curButton)

    if(curButton == 'field_create-card-button'):
        print(isValidSensor(sensor_type, url_plug, ip_address, sensor_name, port=port))
        if(isValidSensor(sensor_type, url_plug, ip_address, sensor_name, port=port)):
            print('adding to config')
            if(sensor_type == 'other-type'):
                sensor_type = new_type

            print('adding to config')
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


    #print('(handle_edit_button) curButton: ', curButton)

    if(curButton == 'edit-card-button'):
        sensorType, sensorName = curId['index'].split('`')
        config = db.getSensorConfig(sensorName, sensorType)

        fieldsMap = {}
        fieldsMap['edit_sensor-name'] = config['name']
        #fieldsMap['edit_types-dropdown'] = config['type']
        fieldsMap['edit_ip-address'] = config['address']
        fieldsMap['edit_port-number'] = config['port']
        fieldsMap['edit_url-plug'] = config['sub_address']
        fieldsMap['edit_units'] = config['units']
        fieldsMap['edit_alert'] = config['alerts']
        fieldsMap['edit_minimum-bound'] = config['min_threshold']
        fieldsMap['edit_maximum-bound'] = config['max_threshold']

        print('getSensorConfig({}, {}) = {}'.format(sensorType, sensorName, config))

        return populateEditCard(fieldsMap, curId)
    else:
        return NU


@app.callback(
        [
            Output('editCardMessenger','children'),
            Output('edit_invalid-selection', 'style'),
        ],
        [
            Input('edit_save-card-button', 'n_clicks'),
            #Input('edit_types-dropdown', 'value'),
        ],
        [
            State('edit_sensor-name', 'value'),
            #State('edit_new-type', 'value'),
            State('edit_units', 'value'),
            State('edit_ip-address', 'value'),
            State('edit_port-number', 'value'),
            State('edit_url-plug', 'value'),
            State('edit_minimum-bound', 'value'),
            State('edit_maximum-bound', 'value'),
            State('edit_alert', 'on'),
            State('edit_name-passer', 'children'),
        ]
)
def save_edit_card(save_button, #sensor_type,
        sensor_name, units, ip_address, port, url_plug, min_bound, max_bound, alert,
        type_name_pair):
    ctx = dash.callback_context
    curButton = '';
    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]
    #print('(save_edit_card) curButton: ', curButton)

    try:
        min_bound = float(min_bound)
    except:
        pass
    try:
        max_bound = float(max_bound)
    except:
        pass

    if(curButton == 'edit_save-card-button' and save_button != None):
        oldSensorType, oldSensorName = type_name_pair.split('`')

        valid = isValidSensor(oldSensorType, url_plug, ip_address, sensor_name, port=port)
        print("isValidSensor: {}\nsensor_type: {}, url_plug: {}, ip_address: {}, sensor_name: {}, port: {}".
                format(valid, oldSensorType, url_plug, ip_address, sensor_name, port))
        if(valid):

            old_config = db.getSensorConfig(oldSensorName, oldSensorType)

            if(old_config):
                if(sensor_name == old_config['name']):
                    db.saveConfigData(oldSensorType, sensor_name, 'category', ip_address, port, url_plug, min_bound, max_bound, units, alert)
                else:
                    db.editConfigData(old_config, oldSensorType, sensor_name, 'category', ip_address, port, url_plug, min_bound, max_bound, units, alert)
            else:
                db.saveConfigData(oldSensorType, sensor_name, 'category', ip_address, port, url_plug, min_bound, max_bound, units, alert)

            return [html.Div(), NU, ]

        else:
            return [NU, {'display':'block', 'color': 'red'}, ]

    return NU


@app.callback(
        Output('deleteCardMessenger', 'children'),
        Input('edit_delete-button', 'n_clicks'),
        State('edit_name-passer', 'children'),
)
def handle_delete_button(delete_button, cardName):
    ctx = dash.callback_context
    curButton = '';
    if ctx.triggered:
        curButton = ctx.triggered[0]['prop_id'].split('.')[0]
    #print('(handle_delete_button) curButton: ', curButton)

    if(curButton == 'edit_delete-button' and delete_button != None):
        #print(cardName)
        sensorType, sensorName = cardName.split('`')
        #print("cardName: {} {}".format(sensorName, sensorType))
        db.deleteConfigData(sensorName, sensorType)
        return [html.Div()]

    return NU


@app.callback(
        Output({'type': 'sensor-data', 'index': MATCH}, 'children'),
        Input('interval-component', 'n_intervals'),
        State({'type': 'sensor-data', 'index': MATCH}, 'id'),
)
def live_data_update(numRefreshes, curId):
    sensorType, sensorName = curId['index'].split('`')

    curSensor = db.getSensorConfig(sensorName, sensorType)
    curUnits = Units(sensorType, curSensor['units'])
    cardData = curUnits.convert_to_string(db.getMostRecentSensorData(sensorName, sensorType))

    return cardData

if __name__ == "__main__":
    ip_address = check_output(["hostname", "-I"]).decode("utf-8").split(" ")[0]
    print("IP Address: ", ip_address)
    port = 8050
    print("Port: ", port)
    try:
        f = open("tmp.txt", "w")
        f.write("http://"+str(ip_address)+":"+str(port))
        f.close()
    except:
        print("Please refer to terminal for user interface address")
    app.run_server(debug=True, host=ip_address, port=port)
