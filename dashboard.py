import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, ALL, callback
from dash_bootstrap_components._components.Container import Container

from interactive_wordcloud import create_wordcloud
from modal import create_modal
from the_list import create_list, profile_details
import app

# membuat word cloud
wordcloud = create_wordcloud()

content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div([wordcloud], style={"margin":"10px"})),
                dbc.Col(
                    html.Div(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(id="card-header"),
                                    dbc.CardBody(id="list-card", style={"overflowY":"scroll"})
                                ], 
                                className="w-75 mb-3",
                                style={"height":"400px", "margin":"10px"}
                            )
                        ]
                    )
                )
            ]
        )
    ]
)

#modals = data_modals()
modal = create_modal()
#list_prop = html.Div(id="list-prop")
show_prof = html.Div(id="show-profile")
store = dcc.Store(id="item-store", data=None)

layout = html.Div(
    [content, store, show_prof, modal]
)

# view list people
@callback(
    [
        Output("list-card", "children"),
        Output("card-header", "children")
    ],
    [Input("cloud", "click")]
)
def show_list(item):
    if item:
        list_data = create_list(item[3])
        list_group = dbc.ListGroup(
            [
                *list_data
            ],
            id="list-group",
            flush=True,
        )
        return list_group, item[0]
    return "The list of people will appear here", "Select a word cloud"

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