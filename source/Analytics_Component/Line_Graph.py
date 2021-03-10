

def data_over_time(type, name, hours):
    import plotly.express as px
    from Database import Database

    # instantiate database and connect
    db = Database()
    db.connect()

    data = db.GetRecentSensorData(name, type, int(hours))

    # create line graph
    title_str = name + ": data over " + str(hours) + " hours"
    graph = px.line(data, x='time', y='value', title = title_str)
    return graph
