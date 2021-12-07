import requests
import csv
import pandas as pd
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Show Data Table and Principal Component Analysis"""

    # Download links from Network tab of Developer Tools
    # Source: https://www.reddit.com/r/html5/comments/9f8knj/how_do_i_find_hidden_download_links_on_click_to/


    neutral = ["facebook", "Facebook", "facebook meta", "facebook meta stock", "facebook stock", "Meta"]
    positive = ["facebook up", "Facebook up", "facebook meta up", "facebook stock up", "Meta up", "facebook increase", "Facebook increase", "Meta increase"]
    negative = ["facebook down", "Facebook down", "facebook meta down", "facebook stock down", "Meta down", "facebook decrease", "Facebook decrease", "Meta decrease"]

    url_neut = ["https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A22%5C%5C%3A15%202021-12-07T01%5C%5C%3A22%5C%5C%3A15%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAIx6YM8KmNSJf8KZBzHm71vNte3hVb&tz=300", "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A23%5C%5C%3A28%202021-12-07T01%5C%5C%3A23%5C%5C%3A28%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22Facebook%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAJEM6IOWk6bQovTrfM83FtAnDQcNgS&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A24%5C%5C%3A15%202021-12-07T01%5C%5C%3A24%5C%5C%3A15%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%20meta%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAJP-snZWQpXyKTBmO8u9i5wW2-RUbc&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A24%5C%5C%3A43%202021-12-07T01%5C%5C%3A24%5C%5C%3A43%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%20meta%20stock%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAJW8RJtqL2b4sFZB7dxB5sH38V2APT&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A25%5C%5C%3A06%202021-12-07T01%5C%5C%3A25%5C%5C%3A06%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%20stock%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAJcvVLy52tdst3WmyPXfjqcU22HpVf&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A25%5C%5C%3A26%202021-12-07T01%5C%5C%3A25%5C%5C%3A26%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22ENTITY%22%2C%22value%22%3A%22%2Fm%2F0hmyfsv%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAJhnx3taUi1r_P3Mypl_c9zh-hf_g9&tz=300" \
    ]

    url_pos = \
    [ \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A26%5C%5C%3A49%202021-12-07T01%5C%5C%3A26%5C%5C%3A49%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%20up%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAJ2ej335jF030HwQ_lm5bL8kAPOpxA&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A27%5C%5C%3A26%202021-12-07T01%5C%5C%3A27%5C%5C%3A26%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22Facebook%20up%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAJ_jSPgEw4ULhxRr45AU-3bSsXVKWn&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A28%5C%5C%3A21%202021-12-07T01%5C%5C%3A28%5C%5C%3A21%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%20meta%20up%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAKNWiydCd6gd95XExTb55xan1S6Lxs&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A29%5C%5C%3A51%202021-12-07T01%5C%5C%3A29%5C%5C%3A51%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%20stock%20up%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAKjxTxrFy3ncESxhR8SgGnq2GIuHuJ&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A30%5C%5C%3A13%202021-12-07T01%5C%5C%3A30%5C%5C%3A13%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22Meta%20up%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAKpUXMvMkXUJqjD6NHnOJHDvHEPBjO&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A30%5C%5C%3A36%202021-12-07T01%5C%5C%3A30%5C%5C%3A36%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%20increase%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAKvAbSf92KbU5wQovzi5XN-nTs8r5Z&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A30%5C%5C%3A57%202021-12-07T01%5C%5C%3A30%5C%5C%3A57%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22Facebook%20increase%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAK0fwzCNSo9pLCeunAVeQexKMzjtEA&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A31%5C%5C%3A12%202021-12-07T01%5C%5C%3A31%5C%5C%3A12%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22Meta%20increase%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAK4PqP36Xbs1aSffffPAsOvNhQW-PY&tz=300" \
    ]

    url_neg = \
    [ \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A31%5C%5C%3A51%202021-12-07T01%5C%5C%3A31%5C%5C%3A51%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%20down%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbALB56GYN31l5SIxpfEqpsdKWiayrq-&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A32%5C%5C%3A10%202021-12-07T01%5C%5C%3A32%5C%5C%3A10%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22Facebook%20down%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbALGvaOpMOHCG-KdhfLcDNy9jUoUAPL&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A32%5C%5C%3A32%202021-12-07T01%5C%5C%3A32%5C%5C%3A32%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%20meta%20down%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbALMJZCo1I2PSwpbpdBOqls9XyJNr0Q&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A32%5C%5C%3A54%202021-12-07T01%5C%5C%3A32%5C%5C%3A54%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%20stock%20down%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbALRmUZz-TtXI8iig6YkS4q8RK2vwLD&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A33%5C%5C%3A45%202021-12-07T01%5C%5C%3A33%5C%5C%3A45%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22Meta%20down%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbALefZXHWiUayOVxfXRGiYMFbc7a6kU&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A34%5C%5C%3A23%202021-12-07T01%5C%5C%3A34%5C%5C%3A23%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%20decrease%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbALnwwjdHQE8Xos5-stjKcuTfjVXmb9&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A34%5C%5C%3A50%202021-12-07T01%5C%5C%3A34%5C%5C%3A50%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22Facebook%20decrease%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbALugVYI1qiXzZRBinYphOS1-4BYz8m&tz=300", \
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-30T01%5C%5C%3A35%5C%5C%3A29%202021-12-07T01%5C%5C%3A35%5C%5C%3A29%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22Meta%20decrease%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYbAL4W9E3ffdhw2lHjMaglGJmaS4IFi6&tz=300" \
    ]


    ### Creating header row using search term facebook

    url = url_neut[0]
    r = requests.get(url, allow_redirects=True)
    open("facebook_lowercase.csv", "wb").write(r.content)

    # Source: https://stackoverflow.com/questions/59970956/delete-first-rows-of-csv-file-in-python
    with open("facebook_lowercase.csv","r") as f, open("facebook_lowercase_temp.csv","w") as f1:
        for i in range(3):
            next(f) # skip header line
        for line in f:
            # Only hours that stock market is open
            if ("T10," in line) or ("T11," in line) or ("T12," in line) or ("T13," in line) or ("T14," in line) or ("T15," in line) or ("T16," in line):
                f1.write(line)

    # Create header row of final csv
    # Source: https://stackoverflow.com/questions/39662891/read-in-the-first-column-of-a-csv-in-python/39662990
    with open("facebook_lowercase_temp.csv","r") as f, open("final.csv","w") as f1:
        csv_reader = csv.reader(f, delimiter=",")
        # Leave space for first empty entry of first row
        f1.write(' ')
        for row in csv_reader:
            # Convert time to datetime format
            # Source: https://stackabuse.com/converting-strings-to-datetime-in-python/
            if datetime.datetime.strptime(row[0], "%Y-%m-%dT%H").weekday() < 5:
                f1.write("," + str(datetime.datetime.strptime(row[0], "%Y-%m-%dT%H")))
        f1.write(",target\n")


    ### For all neutral search terms
    len_neut = len(neutral)
    for i in range(len_neut):
        url = url_neut[i]
        r = requests.get(url, allow_redirects=True)
        filename = "neut" + str(i) + ".csv"
        filetemp = "neut" + str(i) + "temp.csv"
        open(filename, "wb").write(r.content)

        with open(filename,"r") as f, open(filetemp,"w") as f1:
            for i in range(3):
                next(f) # skip header lines
            for line in f:
                # Only hours that stock market is open
                if ("T10," in line) or ("T11," in line) or ("T12," in line) or ("T13," in line) or ("T14," in line) or ("T15," in line) or ("T16," in line):
                    f1.write(line)

        with open(filetemp,"r") as f, open("final.csv","a") as f1:
            csv_reader = csv.reader(f, delimiter=",")
            f1.write('facebook')
            for row in csv_reader:
                if datetime.datetime.strptime(row[0], "%Y-%m-%dT%H").weekday() < 5:
                    f1.write("," + row[1])
            f1.write(",neutral")


    # Source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_html.html
    # to read csv file
    a = pd.read_csv("final.csv")

    # Assign table to a variable
    table = a.to_html(index=False)

    # Render page
    return render_template("index.html", table=table)





@app.route("/about", methods=["GET"])
def about():
    """Show Data Table and Principal Component Analysis"""

    # Render page
    return render_template("about.html")