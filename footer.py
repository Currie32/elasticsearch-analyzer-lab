from dash import dcc, html


footer = html.Div(id='footer', children=[
    html.P("Elasticsearch Analyzer Lab. All rights reserved."),
    html.Div("|", className="footer-pipe"),
    html.A("We're open source!", target="_blank", href="https://github.com/Currie32/elasticsearch-analyzer-lab"),
    html.Div("|", className="footer-pipe"),
    html.A(
        html.Img(src='assets/buyMeACoffee.png', alt='Link to Currie32 Buy me a Coffee page.', id="buy-me-a-coffee-logo"),
        target="_blank",
        href="https://www.buymeacoffee.com/Currie32",
    ),
    html.Div("|", className="footer-pipe"),
    html.P("david.currie32@gmail.com"),
])
