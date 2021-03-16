

def data_over_time(type, name, hours, visible=True):
    #import plotly.express as px
    import plotly.graph_objects as go
    from Database import Database
    from timeKeeper import TimeStamps

    # instantiate database and connect
    db = Database()
    db.connect()

    # getting data about sensor
    all_vals = db.getRecentSensorData(name, type, int(hours))
    # check for emty set
    if len(all_vals) == 0:
        print("Sensor not found in database")
        return None

    max_val  = db.getRecentMax(name, type, int(hours))
    min_val  = db.getRecentMin(name, type, int(hours))


    fig = go.Figure()
    # create datasets for the graph lines and add to graph
    # all values
    x = []                      # X-coordinate
    y = []                      # Y-coordinate
    ts = TimeStamps()
    for i in all_vals:
        x.append(ts.stringToTimestamp(i['time']))
        y.append(i['value'])

    # get avg dataset
    run_avg = [0]*len(y)     # hold a running avg of the data
    sum = 0.                    # for calculating avg
    cnt = 0                     # counter for loop
    for i in range(len(y)-1,-1,-1):
        cnt += 1
        sum += y[i]
        run_avg[i] = (sum/cnt)

    # data line
    fig.add_trace(go.Scatter(x=x, y=y, name='Sensor Data', visible=visible,
                             line=dict(shape='spline',
                             color='darkslateblue', width=2)))

    # avg line
    fig.add_trace(go.Scatter(x=x, y=run_avg,
                             name='Average: '+str(round(db.getAvgVal(name,type),2)),
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
                                   yaxis_title=type)

    return fig



## with buttons for day week month year
def with_buttons(type, name):
    import plotly.graph_objects as go


    # create the day graph
    day_fig = data_over_time(type, name, 24, visible=False)
    # changing name to match the buttons
    day_fig['data'][0]['name'] = "day"


    # create the week graph
    week_fig = data_over_time(type, name, 24*7, visible=False)
    # changing name to match the buttons
    week_fig['data'][0]['name'] = "week"

    # create the month graph (assume all months are 30 days)
    month_fig = data_over_time(type, name, 24*30, visible=False)
    # changing name to match the buttons
    month_fig['data'][0]['name'] = "month"

    # create the year graph (assume all years are 365)
    year_fig = data_over_time(type, name, 24*365)
    # changing name to match the buttons
    year_fig['data'][0]['name'] = "year"

    # create the frankenstein graph
    all_fig = go.Figure()
    # add the day trace
    all_fig.add_trace(day_fig['data'][0])
    # add the week trace
    all_fig.add_trace(week_fig['data'][0])
    # add the month trace
    all_fig.add_trace(month_fig['data'][0])
    # add the year trace
    all_fig.add_trace(year_fig['data'][0])

    # add the buttons
    all_fig.update_layout(
        updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.7,
            y=1.2,
            showactive=True,
            buttons=list(
                [
                    dict(
                        label="day",
                        method="update",
                        args=[
                            {"visible": [True, False, False, False]},
                        ],
                    ),
                    dict(
                        label="week",
                        method="update",
                        args=[
                            {"visible": [False, True, False, False]},
                        ],
                    ),
                    dict(
                        label="month",
                        method="update",
                        args=[
                            {"visible": [False, False, True, False]},
                        ],
                    ),
                    dict(
                        label="year",
                        method="update",
                        args=[
                            {"visible": [False, False, False, True]},
                        ],
                    ),
                ]
            ),
        )
        ]
    )

    all_fig.show()
