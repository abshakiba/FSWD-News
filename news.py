#!/usr/bin/env python3

from flask import Flask, request, redirect, url_for

from newsdb import get_views, get_authors, get_error

app = Flask(__name__)

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>News Report</title>
  </head>
  <body>
    <!-- results will go here -->
  1. What are the most popular thress articles of all time?<br>
  <br>
  %s
  <br>
  2. Who are the most popular article authors of all time?<br>
  <br>
  %s
  <br>
  3. On which days did more than 1&#37 of requests lead to error?<br>
  <br>
  %s
  </body>
</html>
'''
REPORT = "%s - %s views<br>"
AUTHOR = "%s - %s views<br>"
ERROR = "%s - %s&#37 errors<br>"


@app.route('/', methods=['GET'])
def main():
    '''Main page of the forum.'''
    #  posts = "".join(POST % (date, text) for text, date in get_posts())
    views = "".join(REPORT % (title, views) for title, views in get_views())
    authors = "".join(AUTHOR % (name, views) for name, views in get_authors())
    error = "".join(ERROR % (date, percent) for date, percent in get_error())
    html = HTML_WRAP % (views, authors, error)
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
