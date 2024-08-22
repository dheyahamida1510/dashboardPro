import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, callback
from dash_bootstrap_components._components.Container import Container
import json

from navbar import create_navbar
import app


with open("D:\\Dokumen\\example.json") as pd:
    data = json.load(pd)

data.sort(key= lambda x:x["name"])

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

layout = html.Div(
    [
        dbc.Card(
            [
                list_group
            ],
            className="w-50 mb-3",
            style={"height":"400px", "margin":"10px"}
        )
    ]
)