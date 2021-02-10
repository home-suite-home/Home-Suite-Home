#!/usr/bin/env python
import os

import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from Email_Component import Email_Component

sys.path.append(".")

colors = {"background": "343434"}

app = dash.Dash(
    __name__ 
)


def parse_contents(contents):
    return html.Div(
        [
            html.Img(
                src=contents,
                style={"max-width": "100%", "max-height": "100%", "align": "middle"},
            )
        ]
    )


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
            children=[
                html.Div(
                    [
                        dcc.Input(
                            id="remote-email",
                            placeholder="Input email",
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
                    ],

                ),
            ],
        )
    ]
)

@app.callback(
        [Output(component_id="remote-email", component_property="value")],
        [Input(component_id="button", component_property="n_clicks")],
        [State(component_id="remote-email", component_property="value")],
)
def update_output(n_clicks, remote_email):
    if remote_email != "":
        try:
            print("Sending a test email to " + remote_email)
            confirmation = Email_Component(remote_email)

            print(confirmation.confirmation_email())
        except:
            print("Error: Unable to send a test email to " + remote_email)
        

    return [dash.no_update]




if __name__ == "__main__":
    app.run_server(debug=True)
