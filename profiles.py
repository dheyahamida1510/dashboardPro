import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, callback
from dash_bootstrap_components._components.Container import Container
import json

from navbar import create_navbar

app = dash.Dash(title="CS UPI Alumni Dashboard", external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = create_navbar()

with open("D:\\Dokumen\\example.json") as pd:
    data = json.load(pd)

data_list = []

for index, i in enumerate(data):

    lst = dbc.ListGroupItem(
        [
            html.Div(
                [
                    html.H5(i["name"], className="mb-1"),
                ],
                className="d-flex w-100 justify-content-between",
            ),
            html.P(i["work"], className="mb-1"),
            html.Small(i["location"], className="text-muted"),
        ],
        id={
            "type" : "list",
            "index" : index
        },
        action=True
    )

    data_list.append(lst)

list_group = dbc.ListGroup(
    [
        *data_list
    ]
)

app.layout = html.Div(
    [navbar, list_group],
    style={
        "background": "linear-gradient(to right, #bb88ed, #ffbb00)",
        "height": "100vh"
    }
)

if __name__ == "__main__":
    app.run_server(debug=True)