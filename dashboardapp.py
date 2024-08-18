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
                dbc.Col(html.Div([wordcloud, html.H4("", id="report")])),
                dbc.Col(html.Div([dbc.Card(id="list-card")]))
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
"""
# word cloud
@app.callback(
    Output("report", "children"),
    Input("cloud", "click")
)
def update_output_div(item):
    if item != None:
        return "People: {}".format(item)
"""
# view list people
@app.callback(
    Output("list-card", "children"),
    Input("cloud", "click")
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
        return list_group

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


"""
@app.callback(
    Output("list-prop", "children"),
    [Input({"type": "list", "index": ALL}, "n_clicks")],
    [State({"type": "list", "index": ALL}, "children")]
)
def display_list_properties(n_list, children_list):
    trigger = dash.callback_context.triggered_id
    if trigger is not None:
        index = trigger["index"]
        n = n_list[index]
        children = children_list[index][0]["props"]["children"][0]["props"]["children"]

        if n:
            modal = create_second_modal(children)
            return modal
    return None

@app.callback(
    Output("modal-2", "is_open"),
    [Input("modal-close-2", "n_clicks")],
    [State("modal-2", "is_open")]
)

def modal_toggle(n, is_open):
    if n:
        return not is_open
    return is_open
"""

"""
@app.callback(
    Output("list-prop", "children"),
    [Input({"type" : "list", "index" : ALL}, "n_clicks_timestamp")],
    [State({"type" : "list", "index" : ALL}, "children")]
)

def show_modal(n_timestamp, content):
    if not n_timestamp and max(content) == 0:
        return None
    else:
        c_index = n_timestamp.index(max(n_timestamp))
        title = content[c_index][0]["props"]["children"]
        body = content[c_index][1]["props"]["children"]

        p_modal = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(title)),
                dbc.ModalBody(body),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id={
                            "type":"close",
                            "index":c_index
                        },
                        className="ms-auto"
                    )
                )
            ],
            id={
                "type":"modal",
                "index":c_index
            },
            is_open=True
        )
        return p_modal

@app.callback(
    Output({"type" : "modal", "index" : MATCH}, "is_open"),
    [Input({"type" : "close", "index" : MATCH}, "n_clicks")],
    [State({"type" : "modal", "index" : MATCH}, "is_open")]
)

def modal_toggle(n, is_open):
    if n:
        return not is_open
    return is_open
"""

"""
@app.callback(
    Output("list-prop", "children"),
    [Input({"type":"list", "index":ALL}, "n_clicks")],
    [State("list-prop", "children")]
)

def prof_modals(n_list, children):
    children = []
    for i, n in enumerate(n_list):
        if n:
            p_modal = dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Head {}".format(i+1))),
                    dbc.ModalBody("Body {}".format(i+1)),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id={
                                "type" : "close",
                                "index" : i+1
                            },
                            className="ms-auto"
                        )
                    )
                ],
                id={
                    "type" : "modal",
                    "index" : i+1
                    },
                    is_open=True
            )
            children.append(p_modal)
    return children

@app.callback(
    Output({"type" : "modal", "index" : MATCH}, "is_open"),
    [Input({"type" : "close", "index" : MATCH}, "n_clicks")],
    [State({"type" : "modal", "index" : MATCH}, "is_open")]
)

def open_modal(n, is_open):
    if n:
        return not is_open
    return is_open
"""

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