import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, ALL
# from dash_bootstrap_components._components.Container import Container

from navbar import create_navbar
from interactive_wordcloud import create_wordcloud
from modal import profile_modal, confirmation_modal, loading_modal
from the_list import create_list, profile_header, profile_details

app = dash.Dash(title="CS UPI Alumni Dashboard", external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = create_navbar()

# membuat word cloud
wordcloud = html.Div(create_wordcloud(), id="wordcloud")

content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            wordcloud
                        ],
                        style={
                            "display": "flex",
                            "align-items": "center",
                            "justify-content": "center",
                            "margin":"10px",
                        }
                    )
                ),
                # Card untuk menampung list alumni
                dbc.Col(
                    html.Div(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H4(id="card-header"), style={"background": "#f3f3f3"}),
                                    dbc.CardBody(id="list-card", style={"overflowY":"scroll"})
                                ], 
                                className="w-75 mb-3 border border-primary",
                                style={
                                    "height":"600px", 
                                    "margin":"10px",
                                }
                            )
                        ],
                        style={
                            "display": "flex",
                            "align-items": "center",
                            "justify-content": "center",
                        }
                    )
                )
            ]
        ),
        # Tombol update data
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dbc.Button(
                                "Update Data", 
                                id="update-data",
                                size="lg", 
                                className="ms-auto col-6", 
                                n_clicks=0
                            ),
                        ],
                        className="mr-auto my-0",
                        style={
                            "align-items": "center",
                            "justify-content": "center",
                            "margin":"10px",
                        }
                    )
                ),
                dbc.Col(
                    html.Div(id="check-confirmation")
                )
            ]
        )
    ],
    style={
        "align-items": "center",
        "justify-content": "center",
    }
)

modal_profile = profile_modal()  # modal untuk menampilkan detail profile
modal_confirmation = confirmation_modal() # modal untuk panel konfirmasi
modal_loading = loading_modal() # modal untuk loading
# show_prof = html.Div(id="show-profile")
store = dcc.Store(id="item-store", data=None) # variabel untuk menampung data indeks profile user
running_script = dcc.Store(id="running-script", data=False)
conf_click = dcc.Store(id="store-conf-clicks", data=0) # variabel untuk menampung data klik pada confirmation panel

# app layout
app.layout = html.Div(
    [navbar, content, store, modal_profile, modal_confirmation, modal_loading, running_script, conf_click],
    style={
        "background": "linear-gradient(to right, #bb88ed, #ffbb00)",
        "height": "100vh",
        "width": "100vw",
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

# UPDATE CONFIRMATION PANEL
# Fungsi untuk membuka dan menutup confirmation panel
# callback
@app.callback(
    Output("confirmation-panel", "is_open"),
    [
        Input("update-data", "n_clicks"),
        Input("yes-update", "n_clicks"),
        Input("no-update", "n_clicks")
    ],
    [State("confirmation-panel", "is_open")]
)
# fungsi
def confirmation_panel(n_open, n_yes, n_no, is_open):

    # menggunakan dash.callback_context untuk menentukan komponen yang akan men-trigger callback
    ctx = dash.callback_context

    if not ctx.triggered:
        return is_open

    # mencari id dari komponen yang melakukan trigger pada callback
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # jika id adalah id button update data (update-data)
    if trigger_id == "update-data":
        # membuka confirmation panel
        return True
    # jika id adalah button yes atau button no
    elif trigger_id in ["yes-update", "no-update"]:
        # menutup confirmation panel
        return False

    return is_open
"""    
@app.callback(
    [
        Output("loading-modal", "is_open"),
        Output("check-confirmation", "children"),
        Output("running-script", "data"),
        Output("wordcloud", "children")
    ],
    [
        Input("yes-update", "n_clicks"),
        Input("running-script", "data")
    ],
    [
        State("loading-modal", "is_open"),
        State("wordcloud", "children")
    ]
)
def update_confirmation(n, running_script, is_open, content):
    # menggunakan dash.callback_context untuk menentukan komponen yang akan men-trigger callback
    ctx = dash.callback_context

    if not ctx.triggered:
        return is_open, "", running_script, content

    # mencari id dari komponen yang melakukan trigger pada callback
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "yes-update" and n > 0 and running_script == False:
        return True, "", True, content

    elif trigger_id == "running-script" and running_script == True and is_open == True:
        isolated_variables = {}
        with open("D:\\Dokumen\\dashboardPro\\test_1.py", "r") as scp:
            code_script = scp.read()
            exec(code_script, isolated_variables, isolated_variables)
        with open("D:\\Dokumen\\dashboardPro\\data_classification_rev.py", "r") as scp:
            code_script = scp.read()
            exec(code_script, isolated_variables, isolated_variables)
        return False, "Action!", False, create_wordcloud()

    return is_open, "", running_script, content
"""
# Fungsi untuk check konfirmasi update data
# callback
@app.callback(
    Output("wordcloud", "children"),
    [Input("yes-update", "n_clicks")],
    [State("wordcloud", "children")]
)
# fungsi
def update_confirmation(n, content):
    # jika tombol yes di-click
    if n > 0:
        isolated_variables = {}
        with open("D:\\Dokumen\\dashboardPro\\test_1.py", "r") as scp:
            code_script = scp.read()
            exec(code_script, isolated_variables, isolated_variables)
        with open("D:\\Dokumen\\dashboardPro\\data_classification_rev.py", "r") as scp:
            code_script = scp.read()
            exec(code_script, isolated_variables, isolated_variables)
        return create_wordcloud()
    return content

# WORD CLOUD
# Fungsi untuk menampilkan list alumni dengan klik word cloud
# callback
@app.callback(
    [
        Output("list-card", "children"),
        Output("card-header", "children")
    ],
    [Input("cloud", "click")]
)
# fungsi
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

# Fungsi untuk menampilkan dan menutup modal detail profile alumni
# callback
@app.callback(
    [
        Output("modal", "is_open"),
        Output("modal-header", "children"),
        Output("modal-body", "children"),
        Output({"type": "list", "index": ALL}, "n_clicks")
    ],
    [
        Input({"type": "list", "index": ALL}, "n_clicks"),
        Input("modal-close", "n_clicks")
    ],
    [
        State({"type": "list", "index": ALL}, "children"),
        State("modal", "is_open")
    ]
)
# fungsi
def modal_toggle(n_list, n_close, content, is_open):

    # Fungsi untuk menutup modal
    # menggunakan dash.callback_context untuk menentukan komponen yang akan men-trigger callback
    ctx = dash.callback_context
    # jika callback context tidak mengalami trigger
    if not ctx.triggered:
        # tidak melakukan apapun
        return is_open, "", "", n_list

    # mencari id dari komponen yang melakukan trigger pada callback
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    # jika id adalah id button untuk menutup modal (modal-close)
    if trigger_id == "modal-close":
        # tutup modal dan reset komponen n_clicks dari list profile user
        return False, "", "", [0]*len(n_list)

    # Fungsi untuk mengisi dan membuka modal
    # Memeriksa komponen n_clicks pada list profile user
    for i, n in enumerate(n_list):
        # jika terdapat komponen n_clicks yang tidak NONE dan tidak bernilai 0
        if n and n > 0:
            # Membuat detail profile
            # mendapatkan nama user melalui children dari list profile user
            name = content[i][0]["props"]["children"][0]["props"]["children"]
            header = profile_header(name)
            # membuat detail profile user berupa list experience
            body = profile_details(name)
            # membuka modal dan menuliskan detail profile pada modal, reset n_clicks
            return True, header, body, [0]*len(n_list)

    return is_open, "", "", n_list

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
    app.run_server()