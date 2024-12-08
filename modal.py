#import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
#rom interactive_wordcloud import create_wordcloud

#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

def profile_modal():
    modal = html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(id="modal-header", className="border border-primary", style={"background": "#f3f3f3"}),
                    dbc.ModalBody(id="modal-body"),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id="modal-close",
                            className="ms-auto",
                            n_clicks=0,
                        ),
                        className="border border-primary",
                        style={"background": "#f3f3f3"}
                    ),
                ],
                id="modal",
                size="lg",
                scrollable=True,
                is_open=False,
            ),
        ]
    )
    return modal

def confirmation_modal():
    modal = html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div(
                                            "Are you sure want to update data?", 
                                            className="mx-auto mb-2",
                                            style={
                                                "display": "flex",
                                                "align-items": "center",
                                                "justify-content": "center",
                                            },                                                           
                                        ),
                                    ),
                                ],
                                className="pb-2",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "No",
                                                    id="no-update",
                                                    className="col-6",
                                                    n_clicks=0,
                                                    color="dark",
                                                    outline=True,
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "align-items": "center",
                                                "justify-content": "center",
                                            }                                                            
                                        ),
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Yes",
                                                    id="yes-update",
                                                    className="col-6",
                                                    n_clicks=0,
                                                    color="primary",
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "align-items": "center",
                                                "justify-content": "center",
                                            }
                                        ),
                                    ),                                                                                                
                                ],
                                className="py-2",
                            ),
                        ],
                    ),
                ],
                id="confirmation-panel",
                centered=True,
                is_open=False
            )
        ]
    )
    return modal

def loading_modal():
    modal = html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div(
                                            "Updating Data...", 
                                            className="mx-auto mb-2",
                                            style={
                                                "display": "flex",
                                                "align-items": "center",
                                                "justify-content": "center",
                                            },
                                        )
                                    )
                                ],
                                className="pb-2"
                            )
                        ]
                    )
                ],
                id="loading-modal",
                centered=True,
                is_open=False,
                keyboard=False,
                backdrop="static"
            )
        ]
    )
    return modal
"""
def create_second_modal(item):
    modal = html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle(item)),
                    dbc.ModalBody(item),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id="modal-close-2",
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ),
                ],
                id="modal-2",
                scrollable=True,
                fullscreen=True,
                is_open=False,
            ),
        ]
    )
    return modal
"""

"""
def create_custom_modal(name, content, order):
    modal = html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle(name)),
                    dbc.ModalBody(content),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id="close-body-{}".format(order+1),
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ),
                ],
                id="modal-body-{}".format(order+1),
                scrollable=True,
                is_open=False,
            ),
        ]
    )
    return modal

def data_modals():
    wc_list = create_wordcloud().list
    modals = []

    for index, content in enumerate(wc_list):
        if len(content[3]) > 0:
            modals.append(create_custom_modal(content[0], content[3], index))

    return modals

"""