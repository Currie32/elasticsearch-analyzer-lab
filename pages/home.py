import logging
import json
from typing import Dict, List, Tuple

import dash_bootstrap_components as dbc
from dash import (Input, Output, State, callback, callback_context,
                  clientside_callback, dcc, html, no_update, register_page)
from elasticsearch import Elasticsearch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

register_page(__name__, path="")


# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9200'])
INDEX_NAME = "index"
with open('assets/example_indices.json', 'r') as file:
    logger.info("Loading example indices")
    EXAMPLE_INDICES = json.load(file)
    logger.info(EXAMPLE_INDICES)


layout = html.Div(
    children=[
        # Content section
        html.Div(
            id="content",
            children=[
                html.H1(id="page-header", children=["Build your analyzer and see how it tokenizes a string."]),
                html.P(id="description", children=["Test out different filters and tokenizers to see how they affect the tokens that are produced."]),
                html.P(id="description", children=["Or see some example analyzers by clickin on one of the buttons below."]),
                html.Div(id="example-buttons", children=[
                    # Five example buttons
                    dbc.Button(id="example-button1", children=["Example Analyzer 1"]),
                    dbc.Button(id="example-button2", children=["Example Analyzer 2"]),
                    # dbc.Button(id="example-button3", children=["Example Analyzer 3"]),
                    # dbc.Button(id="example-button4", children=["Example Analyzer 4"]),
                    # dbc.Button(id="example-button5", children=["Example Analyzer 5"]),
                ]),
                dbc.Textarea(id="custom-index", value=json.dumps(EXAMPLE_INDICES['example1'], indent=4), style={"height": "500px"}),
                html.P(id="description", children=["Enter some text to see how your custom analyzer parses it into tokens."]),
                dbc.Textarea(id="user-text", value="The QUICK Brown FoX, jumps over the LAZY DOG"),
                html.Div(id="tokens"),
                html.P(id="error-message", style={"color": "red"}),
            ],
        ),
    ],
)

@callback(
    Output("custom-index", "value"),
    Input("example-button1", "n_clicks"),
    Input("example-button2", "n_clicks"),
    # Input("example-button3", "n_clicks"),
    # Input("example-button4", "n_clicks"),
    # Input("example-button5", "n_clicks"),
    prevent_initial_call=True,
)
def update_output(button1, button2):

    ctx = callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == "example-button1":
            return json.dumps(EXAMPLE_INDICES['example1'], indent=4)
        elif button_id == "example-button2":
            return json.dumps(EXAMPLE_INDICES['example2'], indent=4)
        # elif button_id == "example-button3":
        #     return json.dumps(EXAMPLE_INDICES['example3'], indent=4)
        # elif button_id == "example-button4":
        #     return json.dumps(EXAMPLE_INDICES['example4'], indent=4)
        # elif button_id == "example-button5":
        #     return json.dumps(EXAMPLE_INDICES['example5'], indent=4)


@callback(
    Output("tokens", "children"),
    Output("error-message", "children"),
    Input("custom-index", "value"),
    State("user-text", "value"),
)
def index(
    index_body: str,
    text: str,
):

    logger.info(index_body)
    if es.indices.exists(index=INDEX_NAME):
        logger.info("Deleting index")
        try:
            es.indices.delete(index=INDEX_NAME)
            logger.info("Index deleted")
        except Exception as error:
            logger.info(f"Failed to delete index: {error}")
            pass

    if index_body:
        logger.info("Creating index")
        try:
            es.indices.create(index=INDEX_NAME, body=json.loads(index_body))
            logger.info("Index created")
            response = es.indices.analyze(index=INDEX_NAME, body={'analyzer': "custom_analyzer", 'text': text})
            tokens = [html.Div(token['token']) for token in response['tokens']]
            return tokens, ""

        except Exception as error:
            logger.info(f"Failed to create index: {error}")
            return [], f"An error occurred: {type(error).__name__} - {error}"


@callback(
    Output("tokens", "children", allow_duplicate=True),
    Output("error-message", "children", allow_duplicate=True),
    Input("user-text", "value"),
    prevent_initial_call=True,
)
def start_conversation(
    text: str,
) -> str:

    if text and es.indices.exists(index=INDEX_NAME):
        try:
            response = es.indices.analyze(index=INDEX_NAME, body={'analyzer': "custom_analyzer", 'text': text})
            tokens = [html.Div(token['token']) for token in response['tokens']]
            return tokens, ""

        except Exception as error:
            return [], f"An error occurred: {type(error).__name__} - {error}"

