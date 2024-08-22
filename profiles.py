import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, ALL, callback
from dash_bootstrap_components._components.Container import Container
import json

from navbar import create_navbar
from modal import create_modal
from the_list import profile_details
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

modal = create_modal()
store = dcc.Store(id="item-store", data=None)

layout = html.Div(
    [
        dbc.Card(
            [
                list_group,
                modal,
                store
            ],
            className="w-50 mb-3",
            style={"height":"400px", "margin":"10px"}
        )
    ]
)

"""
# modal untuk view profile
@callback(
    [
        Output("modal", "is_open"),
        Output("modal-header", "children"),
        Output("modal-body", "children"),
        Output("item-store", "data"),
        Output({"type": "list", "index": ALL}, "n_clicks")
    ],
    [
        Input({"type": "list", "index": ALL}, "n_clicks"),
        Input("modal-close", "n_clicks")
    ],
    [
        State({"type": "list", "index": ALL}, "children"),
        State("modal", "is_open"),
        State("item-store", "data")
    ]
)

def modal_toggle(n_list, n_close, content, is_open, idx_stored):

    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, "", "", idx_stored, n_list

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "modal-close":
        return False, "", "", idx_stored, [0]*len(n_list)

    for i, n in enumerate(n_list):
        if n and n > 0:
            title = content[i][0]["props"]["children"][0]["props"]["children"]
            body = profile_details(title)
            n_list = [0]*len(n_list)
            return not is_open, title, body, i, n_list

    return is_open, "", "", idx_stored, n_list
"""