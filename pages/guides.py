from dash import (dcc, html, register_page)


register_page(__name__, path="/guides")


layout = html.Div(
    children=[
        html.Div(
            id="content-guide",
            children=[
                html.H1(id="guides-header", children=["Guides for Building Analyzers"]),
                html.Div(id="guide-links", children=[
                    dcc.Link("How the lowercase and uppercase filters impact other filters", href="/lowercase-tokenization"),
                    dcc.Link("How the lowercase and uppercase filters affect tokenization", href="/lowercase-tokenization"),
                    dcc.Link("How the lowercase and uppercase filters affect tokenization", href="/lowercase-tokenization"),
                    dcc.Link("How the lowercase and uppercase filters affect tokenization", href="/lowercase-tokenization"),
                ])
            ]
        )
    ]
)
