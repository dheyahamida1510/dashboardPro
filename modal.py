#import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
#rom interactive_wordcloud import create_wordcloud

#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

def create_modal():
    modal = html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle(id="modal-header")),
                    dbc.ModalBody(id="modal-body"),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id="modal-close",
                            className="ms-auto",
                            n_clicks=0,
                        )
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