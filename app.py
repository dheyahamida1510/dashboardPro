import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dashboard, profiles

from navbar import create_navbar

app = dash.Dash(title="CS UPI Alumni Dashboard", external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

navbar = dbc.NavbarSimple(
    [
        dbc.NavItem(dcc.Link("Dashboard", href="/", className="nav-link")),
        dbc.NavItem(dcc.Link("Alumni Profiles", href="/profiles", className="nav-link"))
    ],
    brand="CS UPI Alumni Dashboard",
    color="dark",
    dark=True
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        html.Div(id="page-content"),
    ],
    style={
        "background": "linear-gradient(to right, #bb88ed, #ffbb00)",
        "height": "100vh",
        "width": "100vw",
    }
)


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)

def show_page(pathname):
    if pathname == "/":
        return dashboard.layout
    elif pathname == "/profiles":
        return profiles.layout
    else:
        return "Page not found"

if __name__ == "__main__":
    app.run_server(debug=True)