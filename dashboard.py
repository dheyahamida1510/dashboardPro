import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, callback
from dash_bootstrap_components._components.Container import Container

from navbar import create_navbar
from interactive_wordcloud import create_wordcloud
from modal import create_modal

navbar = create_navbar()

# membuat word cloud
wordcloud = create_wordcloud()

content = dbc.Container(
    [
        dbc.Row(
            [
                html.Div(
                    [wordcloud, html.H4("", id="report")]
                )
            ]
        )
    ]
)

modal = create_modal()

layout = html.Div(
    [navbar, content, modal],
    style={
        "background": "linear-gradient(to right, #bb88ed, #ffbb00)",
        "height": "100vh"
    }
)
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
# modal
@callback(
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
    if n and is_open:
        return False, None, None
    if item:
        list_data = []
        for i in item[3]:
            list_data.append(dbc.ListGroupItem("{}".format(i)))
        list_group = dbc.ListGroup(
            [
                *list_data
            ]
        )
        return True, "{}".format(item[0]), list_group
    return is_open, None, None
"""
wc_list = create_wordcloud().list

for index, content in enumerate(wc_list):
    if len(content[3])>0:
        @app.callback(
            Output("modal-body-{}".format(index+1), "is_open"),
            [
                Input("cloud", "click"),
                Input("close-body-{}".format(index+1), "n_clicks"),
            ],
            [State("modal-body-{}".format(index+1), "is_open")],
        )

        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open


for i in modals:
    print(i.children)
"""
#===================================================================================
"""
@app.callback(
    Output("modal-body-scroll", "is_open"),
    [
        Input("cloud", "click"),
        Input("close-body", "n_clicks"),
    ],
    [State("modal-body", "is_open")],
)

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
"""