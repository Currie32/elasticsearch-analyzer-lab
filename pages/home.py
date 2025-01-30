import logging
import json

import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import (Input, Output, State, callback, callback_context,
                  clientside_callback, dcc, html, no_update, register_page)
from elasticsearch import Elasticsearch

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the app page
register_page(__name__, path="")

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9200'])
INDEX_NAME = "index"

# Load example indices
with open('assets/example_indices.json', 'r') as file:
    EXAMPLE_INDICES = json.load(file)

# Define the layout
layout = html.Div(
    children=[
        html.Div(
            id="content",
            children=[
                html.H1(id="page-header", children=["Build your analyzer and see how it tokenizes a string."]),
                html.P(id="description", children=["Test out different filters and tokenizers."]),
                html.P(id="description", children=["Or see some example analyzers by clicking on one of the buttons below."]),
                html.Div(id="example-buttons", children=[
                    dbc.Button(id="example-button1", children=["Example Analyzer 1"]),
                    dbc.Button(id="example-button2", children=["Example Analyzer 2"]),
                ]),
                html.Div(
                    id="separate-analyzers",
                    children=[
                        daq.BooleanSwitch(id='separate-analyzers-toggle', on=False, color="rgb(1, 146, 103)", style={"marginRight": "10px"}),
                        html.P("Use separate analyzers for the index and search", style={"fontStyle": "italic"}),
                    ],
                    style={"display": "flex", "margin": "10px 0px"},
                ),
                html.Div(
                    id="custom-indicies",
                    children=[
                        html.Div(
                            id="text-area-container",
                            style={"display": "flex", "position": "relative", "width": "100%"},
                            children=[
                                html.Div(
                                    id="line-numbers",
                                    style={
                                        "width": "30px",
                                        "textAlign": "right",
                                        "paddingRight": "5px",
                                        "fontFamily": "monospace",
                                        "color": "#888",
                                        "overflow": "hidden",
                                        "whiteSpace": "pre",
                                    },
                                ),
                                dcc.Textarea(
                                    id="custom-index",
                                    value=json.dumps(EXAMPLE_INDICES['example1'], indent=2),
                                    tabIndex=2,
                                    persistence=True,
                                    style={"flexGrow": 1, "fontFamily": "monospace", "whiteSpace": "pre", "overflow": "auto"},
                                ),
                            ],
                        ),
                        html.Div(
                            id="text-area-container-search",
                            style={"display": "flex", "position": "relative", "marginTop": "10px", "display": "none"},
                            children=[
                                html.Div(
                                    id="line-numbers-search",
                                    style={
                                        "width": "30px",
                                        "textAlign": "right",
                                        "paddingRight": "5px",
                                        "fontFamily": "monospace",
                                        "color": "#888",
                                        "overflow": "hidden",
                                        "whiteSpace": "pre",
                                        "maxHeight": "500px",
                                    },
                                ),
                                dcc.Textarea(
                                    id="custom-index-search",
                                    value=json.dumps(EXAMPLE_INDICES['example1'], indent=2),
                                    tabIndex=2,
                                    persistence=True,
                                    style={"flexGrow": 1, "fontFamily": "monospace", "whiteSpace": "pre", "overflow": "auto", "display": "none"},
                                ),
                            ],
                        ),
                    ],
                    style={"display": "flex", "flexDirection": "row"},
                ),
                html.P(id="description", children=["Enter some text to see how your custom analyzer parses it into tokens."], style={"fontStyle": "italic", "marginTop": "15px"}),
                html.Div(
                    id="user-texts",
                    children=[
                        dcc.Textarea(id="user-text", value="The QUICK Brown FoX, jumps over the LAZY DOG", persistence=True),
                        dcc.Textarea(id="user-text-search", value="The QUICK Brown FoX, jumps over the LAZY DOG", persistence=True, style={"display": "none"}),
                    ],
                    style={"display": "flex"},
                ),
                html.Div(
                    id="tokens-div",
                    children=[
                        html.Div(id="tokens"),
                        html.Div(id="tokens-search", style={"display": "none"}),
                    ],
                    style={"display": "flex"},
                ),
                html.Div(
                    id="error-message-div",
                    children=[
                        html.P(id="error-message", style={"color": "red"}),
                        html.P(id="error-message-search", style={"color": "red"}),
                    ],
                    style={"display": "flex"},
                ),
            ],
        ),
    ],
)

@callback(
    Output("custom-index", "value"),
    Input("example-button1", "n_clicks"),
    Input("example-button2", "n_clicks"),
    prevent_initial_call=True,
)
def update_custom_index(button1, button2):

    ctx = callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == "example-button1":
            return json.dumps(EXAMPLE_INDICES['example1'], indent=2)
        elif button_id == "example-button2":
            return json.dumps(EXAMPLE_INDICES['example2'], indent=2)


@callback(
    Output('text-area-container-search', 'style'),
    Output('text-area-container', 'style'),
    Output('custom-index-search', 'style'),
    Output('custom-index', 'style'),
    Output('user-text-search', 'style'),
    Output('user-text', "style"),
    Output('tokens-search', 'style'),
    Output('tokens', "style"),
    Input('separate-analyzers-toggle', 'on'),
    prevent_initial_call=True
)
def toggle_index_display(on):
    if on:
        return (
            {"display": "flex", "position": "relative", "minWidth": "50%"},
            {"display": "flex", "position": "relative", "minWidth": "50%"},
            {"width": "100%", 'display': 'block', "margin-left": "5px"},
            {"width": "100%", "marginRight": "5px"},
            {"width": "50%", 'display': 'inline-block', "margin": "15px 0px 10px 5px", "padding": "5px"},
            {"width": "50%", "marginRight": "5px"},
            {"align-items": "flex-start", "flex-wrap": "wrap", "margin-left": "5px", "max-width": "50%"},
            {"max-width": "50%", "paddingRight": "5px"},
        )
    else:
        return (
            {'display': 'none'},
            {"display": "flex", "position": "relative", "width": "100%"},
            {'display': 'none'},
            {"width": "100%"},
            {'display': 'none'},
            {"width": "100%"},
            {'display': 'none'},
            {"width": "100%"},
        )


clientside_callback(
    """
    function(indexValue, searchValue) {
        // Sync scrolling for the main index text area
        const indexTextArea = document.getElementById('custom-index');
        const indexLineNumbers = document.getElementById('line-numbers');
        if (indexTextArea && indexLineNumbers) {
            indexTextArea.onscroll = function() {
                indexLineNumbers.scrollTop = indexTextArea.scrollTop;
            };
        }

        // Sync scrolling for the search index text area
        const searchTextArea = document.getElementById('custom-index-search');
        const searchLineNumbers = document.getElementById('line-numbers-search');
        if (searchTextArea && searchLineNumbers) {
            searchTextArea.onscroll = function() {
                searchLineNumbers.scrollTop = searchTextArea.scrollTop;
            };
        }

        // Return the line numbers for each textarea
        const lineNumbersIndex = indexValue ? indexValue.split("\\n").map((_, i) => (i + 1)).join("\\n") : "";
        const lineNumbersSearch = searchValue ? searchValue.split("\\n").map((_, i) => (i + 1)).join("\\n") : "";
        return [lineNumbersIndex, lineNumbersSearch];
    }
    """,
    [Output("line-numbers", "children"), Output("line-numbers-search", "children")],
    [Input("custom-index", "value"), Input("custom-index-search", "value")]
)


@callback(
    Output("tokens", "children"),
    Output("error-message", "children"),
    Input("custom-index", "value"),
    State("user-text", "value"),
)
def tokenize_wtih_new_index(
    index_body: str,
    text: str,
):
    if es.indices.exists(index=INDEX_NAME):
        try:
            es.indices.delete(index=INDEX_NAME)
        except Exception as error:
            pass

    if index_body:
        try:
            index_body = json.loads(index_body)
            analyzer = list(index_body["settings"]["analysis"]["analyzer"].keys())[0]

            es.indices.create(index=INDEX_NAME, body=index_body)
            response = es.indices.analyze(index=INDEX_NAME, body={'analyzer': analyzer, 'text': text})
            tokens = [html.Div(token['token']) for token in response['tokens']]
            return tokens, ""

        except Exception as error:
            return [], f"An error occurred: {type(error).__name__} - {error}"



@callback(
    Output("tokens-search", "children"),
    Output("error-message-search", "children"),
    Input("custom-index-search", "value"),
    State("user-text-search", "value"),
)
def tokenize_with_new_index_search(
    index_body: str,
    text: str,
):
    if es.indices.exists(index=INDEX_NAME + "_search"):
        try:
            es.indices.delete(index=INDEX_NAME + "_search")
        except Exception as error:
            pass

    if index_body:
        try:
            index_body_dict = json.loads(index_body)
            analyzer = list(index_body_dict["settings"]["analysis"]["analyzer"].keys())[0]

            es.indices.create(index=INDEX_NAME + "_search", body=index_body)
            response = es.indices.analyze(index=INDEX_NAME + "_search", body={'analyzer': analyzer, 'text': text})
            tokens = [html.Div(token['token']) for token in response['tokens']]
            return tokens, ""

        except Exception as error:
            return [], f"An error occurred: {type(error).__name__} - {error}"

    return [], ""


@callback(
    Output("tokens", "children", allow_duplicate=True),
    Output("error-message", "children", allow_duplicate=True),
    Input("user-text", "value"),
    State("custom-index", "value"),
    prevent_initial_call=True,
)
def tokenize_with_new_text(
    text: str,
    index_body: str,
) -> str:

    if text and es.indices.exists(index=INDEX_NAME):
        try:
            index_body = json.loads(index_body)
            analyzer = list(index_body["settings"]["analysis"]["analyzer"].keys())[0]
            response = es.indices.analyze(index=INDEX_NAME, body={"analyzer": analyzer, "text": text})
            tokens = [html.Div(token['token']) for token in response['tokens']]
            return tokens, ""

        except Exception as error:
            return [], f"An error occurred: {type(error).__name__} - {error}"

    return [], ""


@callback(
    Output("tokens-search", "children", allow_duplicate=True),
    Output("error-message-search", "children", allow_duplicate=True),
    Input("user-text-search", "value"),
    State("custom-index-search", "value"),
    prevent_initial_call=True,
)
def tokenize_with_new_text_search(
    text: str,
    index_body: str,
) -> str:

    if text and es.indices.exists(index=INDEX_NAME + "_search"):
        try:
            index_body = json.loads(index_body)
            analyzer = list(index_body["settings"]["analysis"]["analyzer"].keys())[0]
            response = es.indices.analyze(index=INDEX_NAME + "_search", body={"analyzer": analyzer, "text": text})
            tokens = [html.Div(token['token']) for token in response['tokens']]
            return tokens, ""

        except Exception as error:
            return [], f"An error occurred: {type(error).__name__} - {error}"

    return [], ""


@callback(
    Output("tokens", "children", allow_duplicate=True),
    Output("tokens-search", "children", allow_duplicate=True),
    Input("tokens", "children"),
    Input("tokens-search", "children"),
    Input('separate-analyzers-toggle', 'on'),
    prevent_initial_call="initial_duplicate",
)
def update_token_styles(tokens, tokens_search, toggle):

    if not toggle:
        for token in tokens:
            token["props"]["style"] = {"border": "0px"}
        return tokens, tokens_search

    tokens_text = [t["props"]["children"] for t in tokens]
    tokens_search_text = [t["props"]["children"] for t in tokens_search]

    for token in tokens:
        if token["props"]["children"] in tokens_search_text:
            token["props"]["style"] = {"border": "1px solid blue"}
        else:
            token["props"]["style"] = {"border": "0px"}

    for token in tokens_search:
        if token["props"]["children"] in tokens_text:
            token["props"]["style"] = {"border": "1px solid blue"}
        else:
            token["props"]["style"] = {"border": "0px"}

    return tokens, tokens_search
    