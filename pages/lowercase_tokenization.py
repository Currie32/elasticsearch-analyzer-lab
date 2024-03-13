from dash import (dcc, html, register_page)


register_page(__name__, path="/lowercase-tokenization")

CODE_BLOCK1 = """"synonyms_filter": {
    "type": "synonym",
    "synonyms": ["Quick, Fast"]
}
"""
CODE_BLOCK2 = """"pattern_filter": {
   "type": "pattern_replace",
    "pattern": "dog",
    "replacement": "DOG"
}
"""
CODE_BLOCK3 = """"word_delimiter_filter": {
    "type": "word_delimiter",
    "split_on_case_change": true
}
"""
CODE_BLOCK4 = """{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "filter": [
            "lowercase",
            "synonyms_filter",
            "pattern_filter",
            "word_delimiter_filter"
          ],
          "char_filter": [],
          "tokenizer": "whitespace"
        }
      },
      "filter": {
        "pattern_filter": {
          "type": "pattern_replace",
          "pattern": "dog",
          "replacement": "DOG"
        },
        "synonyms_filter": {
          "type": "synonym",
          "synonyms": ["QUICK, fast"]
        },
        "word_delimiter_filter": {
          "type": "word_delimiter",
          "split_on_case_change": true
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "text": {
        "type": "text",
        "analyzer": "custom_analyzer"
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
                html.H1(id="guides-header", children=["How the lowercase and uppercase filters impact other filters"]),
                html.P(children=[
                    "Everything mentioned here can be equally applied to the ",
                    dcc.Link("lowercase", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-lowercase-tokenfilter.html", target="_blank"),
                    " and ",
                    dcc.Link("uppercase", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-uppercase-tokenfilter.html", target="_blank"),
                    " filters. To keep things simple, I’ll only refer to the lowercase filter as that’s the one that I regularly use."
                ]),
                html.P('The lowercase filter is very useful to include in an analyzer as it normalizes the text to a single case. This means that the case of a string won’t affect the ability of a token in the query to match a token in a document. For example, "Vancouver", "vancouver", and "VaNcOuVeR" will all be converted to the same token "vancouver", so they will all match between the query and document.'),
                html.P(children=[
                    'An important effect of the lowercase filter is that it converts the text in filters following it to lowercase. For example, if you have the query "The QUICK Brown FoX, jumps over the LAZY DOG", and want to use the ',
                    dcc.Link("synonym filter", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-tokenfilter.html", target="_blank"),
                    ':'
                ]),
                html.Pre(CODE_BLOCK1),
                html.P('If you use this synonym filter after the lowercase filter, the synonyms will be converted to lowercase and "fast" will be added to your list of tokens. However, if you use the synonym filter before the lowercase filter, then the token "Quick" will not match the token "QUICK", due to the difference in the case, so "fast" will not be added to your list of tokens.'),
                html.P(children=[
                    "If your analyzer must include both lowercase and uppercase text, then you can use the ",
                    dcc.Link("pattern replace filter", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-pattern_replace-tokenfilter.html", target="_blank"),
                    " to convert a token to the case of your choosing. For example, if you wanted to keep the word dog in uppercase, then you could use the filter:"
                ]),
                html.Pre(CODE_BLOCK2),
                html.P(children=[
                    "Lastly, the ",
                    dcc.Link("word delimiter filter", href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-word-delimiter-tokenfilter.html", target="_blank"),
                    " is highly configurable. One of its attributes is the ability to split on case change. However, if you are using the lowercase filter, then you will need to use the word delimiter filter before the lowercase filter to be able to split on case change. Here’s a filter that you can test with:"
                ]),
                html.Pre(CODE_BLOCK3),
                html.P("To summarize, the lowercase filter can be useful to normalize your texts as you no longer have to worry about the case of a token affecting the ability of a query matching to a document. However, using the lowercase filter before other filters will affect their outputs, thus depending on your strategy, the order of your filters can be critical."),
                html.P("Feel free to copy and paste the analyzer below to play around with the filters discussed:"),
                html.Pre(CODE_BLOCK4),
            ]
        )
    ]
)
