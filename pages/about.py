from dash import (dcc, html, register_page)


register_page(__name__, path="/about")


layout = html.Div(
    children=[
        html.Div(
            id="content-guide",
            children=[
                html.H1(id="guides-header", children=["About"]),
                html.P(children=[
                    "The Elasticsearch Analyzer Lab was created to simplify building and testing Elasticsearch analyzers. Although Elasticsearch offers the ",
                    dcc.Link("analyze endpoint", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-analyze.html", target="_blank"),
                    " to help you understand how an analyzer is tokenizing a string, you need to call this API every time you make a change to your analyzer or string to see the effect. This website allows you to see those changes in real time. You're also able to see which tokens will match when you use a different analyzer for indexing and searching."
                ])
            ]
        )
    ]
)
