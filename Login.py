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

import locale
locale.setlocale(locale.LC_ALL, 'en_US')


urls = (
    '/login/', 'param_missing',
    '/login/(.*)/(.*)', 'login_validate',
    '/signup/(.*)/(.*)/(.*)/(.*)', 'signup_user',
    '/userdetails/(.*)/(.*)','user_details',
    '/userdetails','param_missing',
    '/userdetails/','param_missing'
)

app = web.application(urls, globals())


class login_validate:
    def GET(self, userName,userPassword):
        cnxn = pypyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" "Server=52.211.54.45;" "Database=AdaptiveNewsDatabase;" "uid=sa;pwd=cobra@123")
        cursor = cnxn.cursor()
        cursor.execute(
            'select * from [User] where UserName=' + '\'' + userName + '\'' + ' and UserPassword=' + '\'' + userPassword + '\'')

        if cursor.rowcount == 0:
            return json.dumps('Unauthenticated')
        else:
            return json.dumps('Authenticated')


class signup_user:
    def GET(self, userName,userPassword,userAge,userGender):

        cnxn = pypyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" "Server=52.211.54.45;" "Database=AdaptiveNewsDatabase;" "uid=sa;pwd=cobra@123")
        cursor = cnxn.cursor()
        userAge=  str(userAge)


        sql = 'declare @resultString varchar(100) \r\n' \
               'exec sp_signup_user ' + '\'' + userName + '\','  + '\'' + userPassword + '\',' + userAge + ',' + '\'' + userGender + '\','  + '@resultString out \r\n' \
        'select @resultString'

        result = cursor.execute(sql)
        strResulr = result.fetchone()[0]
        cursor.commit()
        return json.dumps(strResulr)

class user_details:
    def GET(self, userName,userPassword):
        arr = []
        cnxn = pypyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" "Server=52.211.54.45;" "Database=AdaptiveNewsDatabase;" "uid=sa;pwd=cobra@123")
        cursor = cnxn.cursor()
        cursor.execute(
            'select * from [User] where UserName=' + '\'' + userName + '\'' + ' and UserPassword=' + '\'' + userPassword + '\'')

        if cursor.rowcount == 0:
            return json.dumps('Unauthenticated')
        else:
            for row in cursor:
                arr.append(row[1])
                arr.append(row[2])
                arr.append(str(row[3]).upper())
        jsonData = []

        jsonData.append({"UserName": arr[0],
                         "Age": arr[1],
                         "Gender": arr[2]
                         })
        return json.dumps(jsonData, indent=2)

class param_missing:
    def GET(self):
            return json.dumps('Parameters missing')



if __name__ == "__main__":
    app.run()