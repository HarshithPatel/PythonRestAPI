#!/usr/bin/env python
import cgi

import web
# import pyodbc
# import adodbapi
import pypyodbc
import requests
import json


# tree = ET.parse('user_data.xml')
# root = tree.getroot()

urls = (
    '/test/', 'testing',
    '/test', 'testing'
)

app = web.application(urls, globals())


class testing:
    def GET(self):
            return 'Web Service is Up'

if __name__ == "__main__":
    app.run()