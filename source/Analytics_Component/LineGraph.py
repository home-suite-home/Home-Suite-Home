

def data_over_time(type, name, hours):
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
    run_avg = []                # hold a running avg of the data
    sum = 0.                    # for calculating avg
    cnt = 0                     # counter for loop
    ts = TimeStamps()
    for i in all_vals:
        cnt += 1
        x.append(ts.stringToTimestamp(i['time']))
        y.append(i['value'])
        sum += i['value']
        run_avg.append(sum/cnt)

    # data line
    fig.add_trace(go.Scatter(x=x, y=y, name='Sensor Data',
                             line=dict(shape='spline',
                             color='darkslateblue', width=2)))

    # avg line
    fig.add_trace(go.Scatter(x=x, y=run_avg,
                             name='Average: '+str(round(db.getAvgVal(name,type),2)),
                             line=dict(shape='spline', color='lightblue', width=4))
    )

    # Max line
    y = [max_val for i in range(len(y))]  # change y to all max_val
    fig.add_trace(go.Scatter(x=x, y=y, name='Max : '+str(max_val),
                  line=dict(color='maroon', width=4, dash='dash'))
    )

    # Min line
    y = [min_val for i in range(len(y))]    # change y to all min_val
    fig.add_trace(go.Scatter(x=x, y=y, name='Min : '+str(min_val),
                  line=dict(color='forestgreen', width=4, dash='dash'))
    )

    # edit the layout
    title_str = "<b>Sensor Name: </b>" + "<b>{name}</b>".format(**locals()) + "<br>"
    title_str += "All Data from " + str(hours) + " Hours" + " Ago" + "<br>"
    title = dict(text=title_str, font=dict(size=25, family='Helvetica'), x=0.5, xref='paper')
    fig.update_layout(title=title, xaxis_title='Date and Time',
                                       yaxis_title=type)

    fig.show()
    return fig
