from main import app
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from utility.utils import DASH_BASE_URL, content
from apps import home_app, tweets_stream_app, analytics_app

# =============================================================================
# DROPDOW-NMENU
# =============================================================================
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href=DASH_BASE_URL)),
        dbc.NavItem(dbc.NavLink("Tweets Stream", href="/tweetsStream", active="exact")),
        dbc.NavItem(dbc.NavLink("Analytics", href="/analytics", active="exact")),
    ],
    brand="Twitter Dashboard",
    color="primary",
    dark=True,
    fluid=False,
    expand='xl',
    light=True,
)

# =============================================================================
# APP
# =============================================================================

app.layout = html.Div([dcc.Location(id="url"), navbar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == DASH_BASE_URL:
        return home_app.layout
    elif pathname == "/tweetsStream":
        return tweets_stream_app.layout
    elif pathname == "/analytics":
        return  analytics_app.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)


