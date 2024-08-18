import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dashboard, profiles

app = dash.Dash(title="CS UPI Alumni Dashboard", external_stylesheets=[dbc.themes.BOOTSTRAP])

il = html.Div(
    [
        dcc.Location(id="url", pathname="/dashboard", refresh=False),
        html.Div(id="content")
    ]
)

app.validation_layout = html.Div(
    [
        il,
        dashboard.layout,
        profiles.layout,
    ]
)

app.layout = il

@app.callback(
    Output("content", "children"),
    Input("url", "pathname")
)

def show_page(pathname):
    if pathname == "/dashboard":
        return dashboard.layout
    elif pathname == "/profiles":
        return profiles.layout
    else:
        return dashboard.layout

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

@app.callback(
    Output("url", "pathname"),
    [
        Input("navbar-header", "n_clicks"),
        Input("profile-menu", "n_clicks")
    ]
)

def page_navigation(n1, n2):
    ctx = dash.callback_context
    if ctx.triggered:
        menu_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if menu_id == "navbar-header":
            return "/dashboard"
        elif menu_id == "profile-menu":
            return "/profiles"
    return dash.no_update

if __name__ == "__main__":
    app.run_server(debug=True)