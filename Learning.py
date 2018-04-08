#!/usr/bin/env python
import web
import xml.etree.ElementTree as ET
# import pyodbc
# import adodbapi
import pypyodbc
import requests
import json
from newsapi import NewsApiClient
import urllib.request
import math

# tree = ET.parse('user_data.xml')
# root = tree.getroot()

import locale
locale.setlocale(locale.LC_ALL, 'en_US')

urls = (
    '/learning/userweights/(.*)/(.*)','get_weights',
    '/learning/userweights/', 'param_missing',
    '/learning/userweights', 'param_missing',
    '/learning/like/(.*)/(.*)/(.*)', 'post_like',
    '/learning/like/', 'param_missing',
    '/learning/like', 'param_missing',
    '/learning/dislike/(.*)/(.*)/(.*)', 'post_dislike',
    '/learning/dislike/', 'param_missing',
    '/learning/dislike', 'param_missing',
    '/learning/setlearning/(.*)/(.*)/(.*)','set_learning',
    '/learning/setlearning/','param_missing',
    '/learning/getlearning/(.*)/(.*)','get_learning',
    '/learning/getlearning/','param_missing'
)

# newsapi = NewsApiClient(api_key='fcd148d3e7a44031b2f7ef24590d12f8')

app = web.application(urls, globals())



class get_weights:
    def GET(self, userName, userPassword):
        cnxn = pypyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" "Server=52.211.54.45;" "Database=AdaptiveNewsDatabase;" "uid=sa;pwd=cobra@123")
        cursor = cnxn.cursor()

        item = []

        cursor.execute(
            'select * from [User] where UserName=' + '\'' + userName + '\'' + ' and UserPassword=' + '\'' + userPassword + '\'')
        if cursor.rowcount == 0:
            return json.dumps('Unauthenticated')
        else:
            for row in cursor:
                userID = row[0]
                break
        cursor.execute('select * from UserWeights where UserID=' + str(userID))
        for row in cursor:
            item.append(row[3])
        jsonData = []

        jsonData.append({"sports": item[0],
                         "entertainment": item[1],
                         "politics": item[2],
                         "technology": item[2],
                         "business": item[2]
                         })
        return json.dumps(jsonData, indent=2)
        # return item

class post_like:
    def GET(self, userName, userPassword, categoryName):
        cnxn = pypyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" "Server=52.211.54.45;" "Database=AdaptiveNewsDatabase;" "uid=sa;pwd=cobra@123")
        cursor = cnxn.cursor()
        print('exec sp_updateWeights ' + '\'' + userName + '\',' + '\'' + userPassword + '\','  + '\'' + categoryName + '\',1,' + '@resultString out \r\n')
        sql = 'declare @resultString varchar(100) \r\n' \
              'exec sp_updateWeights ' + '\'' + userName + '\',' + '\'' + userPassword + '\','  + '\'' + categoryName + '\',1,' + '@resultString out \r\n' \
                                                                                                                                           'select @resultString'
        result = cursor.execute(sql)
        strResulr = result.fetchone()[0]
        cursor.commit()
        print(int(round(1.1)))
        print(int(round(1.8)))
        return json.dumps(strResulr)

class post_dislike:
    def GET(self, userName, userPassword, categoryName):
        cnxn = pypyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" "Server=52.211.54.45;" "Database=AdaptiveNewsDatabase;" "uid=sa;pwd=cobra@123")
        cursor = cnxn.cursor()

        sql = 'declare @resultString varchar(100) \r\n' \
              'exec sp_updateWeights ' + '\'' + userName + '\',' + '\'' + userPassword + '\','  + '\'' + categoryName + '\',0,' + '@resultString out \r\n' \
                                                                                                                                           'select @resultString'
        result = cursor.execute(sql)
        strResulr = result.fetchone()[0]
        cursor.commit()

        return json.dumps(strResulr)


class set_learning:
    def GET(self, userName, userPassword, learningModel):
        learningModel = str(learningModel).lower()
        if not(learningModel == 'low' or learningModel == 'medium' or learningModel == 'high'):
            jsonData = []
            jsonData.append({"Warning": "Choose Level From Below Category",
                             "1": "low",
                             "2": "medium",
                             "3": "high"
                             })
            return json.dumps(jsonData, indent=2)
        cnxn = pypyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" "Server=52.211.54.45;" "Database=AdaptiveNewsDatabase;" "uid=sa;pwd=cobra@123")
        cursor = cnxn.cursor()

        cursor.execute(
            'select * from [User] where UserName=' + '\'' + userName + '\'' + ' and UserPassword=' + '\'' + userPassword + '\'')
        if cursor.rowcount == 0:
            return json.dumps('Unauthenticated')
        else:
            for row in cursor:
                userID = row[0]
                break
        cursor.execute('update [User] set UserLearningRate = ' + '\'' + learningModel + '\'' + ' where UserID=' + str(userID))
        cursor.commit()
        return json.dumps("Succesfully Set", indent=2)


class get_learning:
    def GET(self, userName, userPassword):

        cnxn = pypyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" "Server=52.211.54.45;" "Database=AdaptiveNewsDatabase;" "uid=sa;pwd=cobra@123")
        cursor = cnxn.cursor()

        cursor.execute(
            'select * from [User] where UserName=' + '\'' + userName + '\'' + ' and UserPassword=' + '\'' + userPassword + '\'')
        if cursor.rowcount == 0:
            return json.dumps('Unauthenticated')
        else:
            for row in cursor:
                userID = row[0]
                break
        cursor.execute('select UserLearningRate from [User] where UserID=' + str(userID))
        for row in cursor:
            learningModel = row[0]
            break
        return json.dumps(learningModel, indent=2)


class param_missing:
    def GET(self):
            return 'Parameters missing'

if __name__ == "__main__":
    app.run()