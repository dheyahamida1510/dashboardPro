from dash import html
import dash_bootstrap_components as dbc
from dash import html
from dash_bootstrap_components._components.Container import Container
from PIL import Image

def create_navbar():
    menudrop = dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(
                "Dashboard", id="dashboard-menu"
            ),
            dbc.DropdownMenuItem(
                "Alumni Profiles", id="profile-menu"
            )
        ],
        label="Menu"
    ) 
    # membuat fitur search
    search_ft = dbc.Row(
        [
            dbc.Col(dbc.Input(type="search", placeholder="Search dashboard")),
            dbc.Col(
                dbc.Button(
                    "Search",
                    color="primary",
                    className="ms-2",
                    n_clicks=0
                ),
                width="auto"
            )
        ],
        class_name="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        align="center"
    )

    pil_image = Image.open("D:/Dokumen/dashboardPro/assets/logo_upi.png")

    # membuat navigation bar
    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=pil_image, height="30px")),
                            dbc.Col(dbc.NavbarBrand("Alumni Dashboard", className="ms-2"))
                        ],
                        align="center",
                        className="g-0"
                    ),
                    id="navbar-header"
                ),
                dbc.Row(
                    [
                        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                        dbc.Col(
                            dbc.Collapse(
                                id="navbar-collapse",
                                is_open=False,
                                navbar=True
                            )
                        )
                    ]
                )
            ],
            fluid=True
        ),
        color="dark",
        dark=True
    )

    return navbar