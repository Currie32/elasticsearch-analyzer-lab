import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, page_container
from flask import Flask, send_from_directory

from footer import footer

server = Flask(__name__)
app = Dash(
    __name__,
    use_pages=True,
    pages_folder="pages",
    external_stylesheets=[dbc.icons.BOOTSTRAP, dbc.themes.BOOTSTRAP],
    server=server,
)
app.config.suppress_callback_exceptions = True


@server.route("/robots.txt")
def serve_robots():
    return send_from_directory(".", "robots.txt", mimetype="text/plain")


@server.route("/sitemap.xml")
def serve_sitemap():
    return send_from_directory(".", "sitemap.xml", mimetype="application/xml")


app.index_string = """<!DOCTYPE html>
<html lang="en">
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-5K5QWFEQL1"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-5K5QWFEQL1');
        </script>
        <meta charset="UTF-8">
        <meta name="description" content="Build and test your Elasticsearch analyzer to see how it tokenizes a string.">
        <meta property="og:title" content="Elasticsearch Analyzer Lab">
        <meta property="og:description" content="Build and test your Elasticsearch analyzer to see how it tokenizes a string.">
        <meta property="og:image" content="https://elasticsearchanalyzerlab.xyz/assets/favicon.ico">
        <meta property="og:url" content="https://elasticsearchanalyzerlab.xyz">
        <meta name="twitter:card" content="https://elasticsearchanalyzerlab.xyz/assets/favicon.ico">
        <meta name="twitter:title" content="Elasticsearch Analyzer Lab">
        <meta name="twitter:description" content="Build and test your Elasticsearch analyzer to see how it tokenizes a string.">
        <meta name="twitter:image" content="https://elasticsearchanalyzerlab.xyz/assets/favicon.ico">
        <link rel="canonical" href="https://elasticsearchanalyzerlab.xyz">
        <meta name="robots" content="index, follow">
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

app.layout = html.Div(
    [
        html.Div(
            className="container",
            children=[
                html.Div(
                    id="header",
                    children=[
                        dcc.Link(id="title", href="/", children=html.H1(children="Elasticsearch Analyzer Lab")),
                        dcc.Link(className="nav-title", href="/about", children=html.H3(children="About")),
                        dcc.Link(className="nav-title", href="/guides", children=html.H3(children="Guides")),
                    ],
                ),
                page_container,
                footer,
            ],
        )
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
