import dash_bootstrap_components as dbc
from dash import html
import json
import re

def create_list(item):

    with open("D:\\Dokumen\\dashboardPro\\people_data.json") as pd:
        data = json.load(pd)

    data_list = []

    for index, i in enumerate(item):
        for p in data:
            if i == p["name"]:
                lst = dbc.ListGroupItem(
                    [
                        html.Div(
                            [
                                html.H5(i, className="mb-1", id={"type" : "list-name", "index" : index}),
                            ],
                            className="d-flex w-100 justify-content-between",
                        ),
                        html.P(p["work"], className="mb-1"),
                        html.Small(p["location"], className="text-muted"),
                    ],
                    id={
                        "type": "list", 
                        "index": index
                    },
                    action=True,
                    n_clicks=0,
                    n_clicks_timestamp=0
                )

                data_list.append(lst)

    return data_list

def profile_header(name):

    with open("D:\\Dokumen\\dashboardPro\\people_data.json") as pd:
        data = json.load(pd)

    header = ""

    for p in data:
        if name == p["name"]:
            header = html.Div(
                [
                    html.H3(name, className="mb-1 px-1 pb-1"),
                    html.Div(
                        [
                            html.P(p["work"], className="mb-0"),
                            html.Small(p["location"], className="text-muted"),
                            html.P(
                                [
                                    html.Small(
                                        [
                                            html.A("Go to " + name + "'s " + "LinkedIn profile", href=p["link"], target="_blank")
                                        ]
                                    ),                            
                                ]
                            ),
                        ],
                        className="px-2"
                    )
                ]
            )
    
    return header

def profile_details(name):

    with open("D:\\Dokumen\\dashboardPro\\people_data.json") as pd:
        data = json.load(pd)

    data_list = []
    for p in data:
        if name == p["name"]:
            for index, e in enumerate(p["experiences"]):
                lst = dbc.ListGroupItem(
                    [
                        html.Div(
                            [
                                html.H5(e["name"], className="mb-1"),
                            ],
                            className="d-flex w-100 justify-content-between",
                        ),
                        html.P(e["location"], className="mb-1"),
                        html.Small(e["time"], className="text-muted"),
                    ],
                    id={
                        "type": "experience-list", 
                        "index": index
                    }
                )
                data_list.append(lst)
    list_group = dbc.ListGroup(
        [
            *data_list
        ],
        id="profile-group",
        flush=True
    )
    return list_group