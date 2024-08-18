import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, MATCH, ALL
from dash_bootstrap_components._components.Container import Container

from navbar import create_navbar
from interactive_wordcloud import create_wordcloud
from modal import create_modal
from the_list import create_list, profile_details

app = dash.Dash(title="CS UPI Alumni Dashboard", external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = create_navbar()

# membuat word cloud
wordcloud = create_wordcloud()

content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div([wordcloud])),
                dbc.Col(
                    html.Div(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(id="card-header"),
                                    dbc.CardBody(id="list-card", style={"overflowY":"scroll"})
                                ], 
                                className="w-75 mb-3",
                                style={"height":"400px"} 
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

app.layout = html.Div(
    [navbar, content, store, show_prof, modal],
    style={
        "background": "linear-gradient(to right, #bb88ed, #ffbb00)",
        "height": "100vh"
    }
)

# navigation bar
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")]
)

def show_navbar(n, is_open):
    if n:
        return not is_open
    return is_open


# view list people
@app.callback(
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
@app.callback(
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

# modal
"""
@app.callback(
    Output("modal", "is_open"),
    Output("modal-header", "children"),
    Output("modal-body", "children"),
    [
        Input("cloud", "click"),
        Input("modal-close", "n_clicks"),
    ],
    [State("modal", "is_open")]
)

def show_modal(item, n, is_open):
    print(f"item : {item}, n : {n}, is_open : {is_open}")
    if n and is_open:
        return False, None, None
    if item:
        list_data = create_list(item[3])
        list_group = dbc.ListGroup(
            [
                *list_data
            ],
            id="list-group"
        )
        return True, "{}".format(item[0]), list_group
    return is_open, None, None

"""


"""
@app.callback(
    Output("modal-2", "is_open"),
    [
        Input({"type": "list", "index": MATCH}, "n_clicks"),
        Input("modal-close-2", "n_clicks"),
    ],
    [
        State("modal-2", "is_open"),
        State("modal", "is_open"),
    ],
)

def show_second_modal(n1, n2, is_open_2, is_open_1):
    print(f"n1 : {n1}, n2 : {n2}, is_open_1 : {is_open_1}, is_open_2 : {is_open_2}")
    n1 = n1 or 0
    n2 = n2 or 0
    if is_open_1:
        if n1 > 0:
            return not is_open_2
        elif n2 > 0:
            return False
    return is_open_2
"""

if __name__ == "__main__":
    app.run_server(debug=True)