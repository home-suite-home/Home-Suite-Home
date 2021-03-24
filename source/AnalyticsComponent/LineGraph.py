

def data_over_time(type, name, hours, visible=True):
    import plotly.graph_objects as go
    from Server_Component.Database import Database
    from timeKeeper import TimeStamps
    import math
    from conversions import Units

    # instantiate database and connect
    db = Database()
    db.connect()

    # getting data about sensor
    all_vals = db.getRecentSensorData(name, type, int(hours))
    # check for emty set
    if len(all_vals) == 0:
        print("Sensor not found in database")
        return None

    #max_val  = db.getRecentMax(name, type, int(hours))
    #min_val  = db.getRecentMin(name, type, int(hours))


    fig = go.Figure()
    # create datasets for the graph lines and add to graph
    # all values
    x = []                      # X-coordinate
    y = []                      # Y-coordinate
    ts = TimeStamps()

    # create unit object for y-axis conversion
    units = db.getSensorConfig(name, type)['units']
    convert = Units(type, units)

    # get avg, mx and min dataset
    max_val = 0
    min_val = 1e9
    run_avg = []        # hold a running avg of the data
    sum = 0.                    # for calculating avg
    cnt = 0                     # counter for loop

    for i in reversed(all_vals):
        if (math.isnan(i['value'])):
            continue
        else:
            y.insert(0, convert.convert(i['value']))
        x.insert(0, ts.stringToTimestamp(i['time']))

        cnt += 1
        sum += i['value']
        run_avg.insert(0, sum/cnt)

    if len(y) == 0:
        print("all NaNs")
        return None

    max_val = max(y)
    min_val = min(y)

    # data line
    fig.add_trace(go.Scatter(x=x, y=y, name='Sensor Data', visible=visible,
                             line=dict(shape='spline',
                             color='darkslateblue', width=2)))

    # avg line
    fig.add_trace(go.Scatter(x=x, y=run_avg,
                             name='Average: '+str(round(run_avg[-1])),
                             visible = visible,
                             line=dict(shape='spline', color='lightblue', width=4))
    )

    # Max line
    y = [max_val for i in range(len(y))]  # change y to all max_val
    fig.add_trace(go.Scatter(x=x, y=y, name='Max : '+str(max_val),
                  visible=visible,
                  line=dict(color='maroon', width=4, dash='dash'))
    )

    # Min line
    y = [min_val for i in range(len(y))]    # change y to all min_val
    fig.add_trace(go.Scatter(x=x, y=y, name='Min : '+str(min_val),
                  visible=visible,
                  line=dict(color='forestgreen', width=4, dash='dash'))
    )

    # edit the layout
    title_str = "<b>Sensor Name: </b>" + "<b>{name}</b>".format(**locals()) + "<br>"
    title_str += "All Data from " + str(hours) + " Hours" + " Ago" + "<br>"
    title = dict(text=title_str, font=dict(size=25, family='Helvetica'), x=0.5, xref='paper')
    fig.update_layout(title=title, xaxis_title='Date and Time',
                                   yaxis_title=type + " " + units)

    return fig



## with buttons for day week month year
def with_buttons(type, name):
    import plotly.graph_objects as go
    from timeKeeper import TimeStamps
    from Server_Component.Database import Database

    # create the day graph
    day_fig = data_over_time(type, name, 24)

    # create the week graph
    week_fig = data_over_time(type, name, 24*7, visible=False)

    # create the month graph (assume all months are 30 days)
    month_fig = data_over_time(type, name, 24*30, visible=False)

    # create the year graph (assume all years are 365)
    year_fig = data_over_time(type, name, 24*365, visible=False)

    # create the frankenstein graph
    all_fig = go.Figure()
    '''
    Traces: all_data: 0
            avg_val : 1
            max_val : 2
            min_val : 3
    '''
    # empty trace if there is no data
    x=[]
    y=[]
    empty_trace = go.Scatter(x=x, y=y, name='Sensor Data', visible=False,
                             line=dict(shape='spline',
                             color='darkslateblue', width=2))

    # add the day traces
    if day_fig:
        all_fig.add_trace(day_fig['data'][0])
        all_fig.add_trace(day_fig['data'][1])
        all_fig.add_trace(day_fig['data'][2])
        all_fig.add_trace(day_fig['data'][3])
    else:
        all_fig.add_trace(empty_trace)
        all_fig.add_trace(empty_trace)
        all_fig.add_trace(empty_trace)
        all_fig.add_trace(empty_trace)

    # add the week trace
    if week_fig:
        all_fig.add_trace(week_fig['data'][0])
        all_fig.add_trace(week_fig['data'][1])
        all_fig.add_trace(week_fig['data'][2])
        all_fig.add_trace(week_fig['data'][3])
    else:
        all_fig.add_trace(empty_trace)
        all_fig.add_trace(empty_trace)
        all_fig.add_trace(empty_trace)
        all_fig.add_trace(empty_trace)
    # add the month trace
    if month_fig:
        all_fig.add_trace(month_fig['data'][0])
        all_fig.add_trace(month_fig['data'][1])
        all_fig.add_trace(month_fig['data'][2])
        all_fig.add_trace(month_fig['data'][3])
    else:
        all_fig.add_trace(empty_trace)
        all_fig.add_trace(empty_trace)
        all_fig.add_trace(empty_trace)
        all_fig.add_trace(empty_trace)
    # add the year trace
    if year_fig:
        all_fig.add_trace(year_fig['data'][0])
        all_fig.add_trace(year_fig['data'][1])
        all_fig.add_trace(year_fig['data'][2])
        all_fig.add_trace(year_fig['data'][3])
    else:
        all_fig.add_trace(empty_trace)
        all_fig.add_trace(empty_trace)
        all_fig.add_trace(empty_trace)
        all_fig.add_trace(empty_trace)

    # edit the layout
    # current day
    date = TimeStamps().stringToTimestamp(TimeStamps().getTimestamp())
    #title_str = "<b>Home-Suite-Home Data Analytics</b><br>"
    title_str = "<br>"
    title_str += "Sensor Name: " + "<b>{name}</b>".format(**locals()) + "<br>"
    title_str += "Sensor History Recorded on: " + \
                 "<b>{date}</b>".format(**locals()) + "<br>"
    #title_str += "All Data from " + str(hours) + " Hours" + " Ago" + "<br>"
    units = Database().getSensorConfig(name, type)['units']
    title = dict(text=title_str, font=dict(size=25, family='Helvetica'), x=0.5, y=0.98, xref='paper')
    all_fig.update_layout(title=title, xaxis_title='Date and Time',
                                   yaxis_title=type + " " + units)

    # add the buttons
    all_fig.update_layout(
        updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.56,
            y=-0.25,
            font=dict(size=20),
            bgcolor='lightblue',
            bordercolor='lightslategray',
            borderwidth=4,
            showactive=True,
            buttons=list(
                [
                    dict(
                        label="Day",
                        method="update",
                        args=[
                            {"visible": [True, True, True, True,
                                         False, False, False, False,
                                         False, False, False, False,
                                         False, False, False, False]},
                        ],
                    ),
                    dict(
                        label="Week",
                        method="update",
                        args=[
                            {"visible": [False, False, False, False,
                                         True, True, True, True,
                                         False, False, False, False,
                                         False, False, False, False]},
                        ],
                    ),
                    dict(
                        label="Month",
                        method="update",
                        args=[
                            {"visible": [False, False, False, False,
                                         False, False, False, False,
                                         True, True, True, True,
                                        False, False, False, False]},
                        ],
                    ),
                    dict(
                        label="Year",
                        method="update",
                        args=[
                            {"visible": [False, False, False, False,
                                         False, False, False, False,
                                         False, False, False, False,
                                         True, True, True, True]},
                        ],
                    ),
                ]
            ),
        )
        ]
    )

    #all_fig.show()
    return all_fig
