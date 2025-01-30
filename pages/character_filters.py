from dash import (dcc, html, register_page)


register_page(__name__, path="/character-filters")

CODE_BLOCK1 = """{
    "settings": {
        "analysis": {
            "analyzer": {
                "custom_analyzer": {
                    "tokenizer": "keyword",
                    "char_filter": [
                        "html_strip"
                    ]
                }
            }
        }
    }
}
"""

CODE_BLOCK2 = """{
    "settings": {
        "analysis": {
            "analyzer": {
                "custom_analyzer": {
                    "tokenizer": "keyword",
                    "char_filter": [
                        "html_strip",
                        "mapping_char_filter"
                    ]
                }
            },
            "char_filter": {
                "mapping_char_filter": {
                    "type": "mapping",
                    "mappings": [
                        ", => ",
                        ": => ",
                        “NY => New York”
                    ]
                }
            }
        }
    }
}
"""

CODE_BLOCK3 = """{
    "settings": {
        "analysis": {
            "analyzer": {
                "custom_analyzer": {
                    "tokenizer": "standard",
                    "char_filter": [
                        "html_strip",
                        "pattern_char_filter",
                        "mapping_char_filter"
                    ]
                }
            },
            "char_filter": {
                "mapping_char_filter": {
                    "type": "mapping",
                    "mappings": [
                        ", => ",
                        ": => ",
                        "NY => New York",
                        "- => _"
                    ]
                },
                "pattern_char_filter": {
                    "type": "pattern_replace",
                    "pattern": "(\\\d+)-(?=\\\d)",
                    "replacement": "$1"
                }
            }
        }
    }
}
"""


layout = html.Div(
    children=[
        html.Div(
            id="content-guide",
            children=[
                html.H1(id="guides-header", children=["Tips for using Character Filters"]),
                html.P(children=[
                    dcc.Link("Character Filters", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-charfilters.html", target="_blank"),
                    " should be used when you need to transform your text before it is fed to the tokenizer. This is usually to standardize text or to accommodate the methodology of the tokenizer. As an example, we’ll use the sentence:"
                ]),
                html.Pre("<p>My father-in-law doesn't live in NY, <br>but his phone number is: 123-456-7890</p>"),
                html.P("There are a number of things that we might want to change about this string before it is tokenized, which could include:"),
                html.Ul(
                    children=[
                        html.Li("Removing the HTML tags"),
                        html.Li('Removing punctuation'),
                        html.Li('Replacing “NY” with "New York"'),
                        html.Li("Removing the hyphens in the phone number"),
                    ]
                ),
                html.P(children=[
                    "Starting with removing the HTML tags, Elasticsearch has us covered with the ",
                    dcc.Link("HTML strip character filter", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-htmlstrip-charfilter.html", target="_blank"),
                    ". If we use the following analyzer:"
                ]),
                html.Pre(CODE_BLOCK1),
                html.P("Then the text will change to:"),
                html.Pre('"My father-in-law doesn\'t live in NY, but his phone number is: 123-456-7890"'),
                html.P(children=[
                    "Next, we can make use of the ",
                    dcc.Link("mapping character filter", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-mapping-charfilter.html", target="_blank"),
                    " to remove the punctuation and replace NY with New York:"
                ]),
                html.Pre(CODE_BLOCK2),
                html.P(children=[
                    "Note, if we were to use the ",
                    dcc.Link("standard tokenizer", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-tokenizer.html", target="_blank"),
                    " instead of the ",
                    dcc.Link("keyword tokenizer", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-keyword-tokenizer.html", target="_blank"),
                    ", then we wouldn’t need to remove the comma and colon from the text as the standard tokenizer would do this for us. However, the standard tokenizer would also split “father-in-law” and “123-456-7890” into “father”, “in”, “law”, and “123”, “456”, “7890”, respectively. If we want to use the standard tokenizer, but avoid these strings from being split into tokens, then we can add the mapping “- => _” and a ",
                    dcc.Link("pattern replace character filter", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-pattern-replace-charfilter.html", target="_blank"),
                    " to remove the hyphen between numbers:"
                ]),
                html.Pre(CODE_BLOCK3),
                html.P("Using this analyzer would results in the following tokens:"),
                html.Pre('"My" "father_in_law" "doesn\'t" "live" "in" "New" "York" "but" "his" "phone" "number" "is" "1234567890"'),
                html.P(children=[
                    "Feel free to copy the analyzer above and play around with different filters, tokenizers, and texts. Currently, the generated tokens will be the same if you switch to the ",
                    dcc.Link("whitespace tokenizer", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-whitespace-tokenizer.html", target="_blank"),
                    ". This is because of the of punctuation mappings. If you remove these mappings, you'll see how these two tokenizers differ."
                ]),
            ]
        )
    ]
)
