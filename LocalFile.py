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
    '/test/', 'testing',
    '/test', 'testing',
    '/news/', 'get_news',
    '/news', 'get_news',
    '/news/usermodel/(.*)', 'news_usermodel',
    '/news/user/(.*)/(.*)', 'news_user',
    '/news/usermodel', 'param_missing',
    '/news/user', 'param_missing',
    '/news/usermodel/', 'param_missing',
    '/news/user/', 'param_missing',
    '/login/', 'param_missing',
    '/login/(.*)/(.*)', 'login_validate',
    '/signup/(.*)/(.*)/(.*)/(.*)', 'signup_user',
    '/userdetails/(.*)/(.*)', 'user_details',
    '/userdetails', 'param_missing',
    '/userdetails/', 'param_missing',
    '/learning/userweights/(.*)/(.*)', 'get_weights',
    '/learning/userweights/(.*)/(.*)/', 'get_weights',
    '/learning/userweights/', 'param_missing',
    '/learning/userweights', 'param_missing',
    '/learning/like/(.*)/(.*)/(.*)', 'post_like',
    '/learning/like/', 'param_missing',
    '/learning/like', 'param_missing',
    '/learning/dislike/(.*)/(.*)/(.*)', 'post_dislike',
    '/learning/dislike/', 'param_missing',
    '/learning/dislike', 'param_missing',
    '/learning/setlearning/(.*)/(.*)/(.*)', 'set_learning',
    '/learning/setlearning/', 'param_missing',
    '/learning/getlearning/(.*)/(.*)', 'get_learning',
    '/learning/getlearning/', 'param_missing'

)

# newsapi = NewsApiClient(api_key='fcd148d3e7a44031b2f7ef24590d12f8')

app = web.application(urls, globals())

class testing:
    def GET(self):
            return json.dumps('Web Service is Up')

# Login API

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

# News API

class get_news:
    def GET(self):

        arr= [x[:] for x in [[None] * 5] * 20]


        # Sports
        with urllib.request.urlopen(
                 "https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
            dataSports = json.loads(url.read().decode())

        # entertainment
        with urllib.request.urlopen(
                "https://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
            dataEntertainment = json.loads(url.read().decode())

        # politics
        with urllib.request.urlopen(
                "https://newsapi.org/v2/top-headlines?country=us&category=politics&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
            dataPolitics = json.loads(url.read().decode())

        # technology
        with urllib.request.urlopen(
                "https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
            dataTechnology = json.loads(url.read().decode())

        # business
        with urllib.request.urlopen(
                "https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
            dataBusiness = json.loads(url.read().decode())

        # Sports
        RandomNewsCount = 0
        categoryCount = 0
        for doc in dataSports['articles']:
            categoryName = 'sports'
            if(RandomNewsCount >= 4):
                break
            if (doc['description'] != None and doc['description'] != ""):
                arr[categoryCount+5 * RandomNewsCount][0]= categoryName
                arr[categoryCount+5*RandomNewsCount][1] = categoryCount + 5 * RandomNewsCount+1
                arr[categoryCount+5*RandomNewsCount][2] = doc['title']
                arr[categoryCount+5*RandomNewsCount][3] = doc['description']
                arr[categoryCount + 5 * RandomNewsCount][4] = doc['url']
                RandomNewsCount += 1

        # entertainment
        RandomNewsCount = 0
        categoryCount+=1
        for doc in dataEntertainment['articles']:
            categoryName = 'entertainment'
            if (RandomNewsCount >= 4):
                break
            if (doc['description'] != None and doc['description'] != ""):
                arr[categoryCount + 5 * RandomNewsCount][0]= categoryName
                arr[categoryCount + 5 * RandomNewsCount][1] = categoryCount + 5 * RandomNewsCount+1
                arr[categoryCount + 5 * RandomNewsCount][2] = doc['title']
                arr[categoryCount + 5 * RandomNewsCount][3] = doc['description']
                arr[categoryCount + 5 * RandomNewsCount][4] = doc['url']
                RandomNewsCount += 1


        # politics
        RandomNewsCount = 0
        categoryCount += 1
        for doc in dataPolitics['articles']:
            categoryName = 'politics'
            if (RandomNewsCount >= 4):
                break
            if (doc['description'] != None and doc['description'] != ""):
                arr[categoryCount + 5 * RandomNewsCount][0]= categoryName
                arr[categoryCount + 5 * RandomNewsCount][1] = categoryCount + 5 * RandomNewsCount+1
                arr[categoryCount + 5 * RandomNewsCount][2] = doc['title']
                arr[categoryCount + 5 * RandomNewsCount][3] = doc['description']
                arr[categoryCount + 5 * RandomNewsCount][4] = doc['url']
                RandomNewsCount += 1

        # technology
        RandomNewsCount = 0
        categoryCount += 1
        for doc in dataTechnology['articles']:
            categoryName = 'technology'
            if (RandomNewsCount >= 4):
                break
            if (doc['description'] != None and doc['description'] != ""):
                arr[categoryCount + 5 * RandomNewsCount][0]= categoryName
                arr[categoryCount + 5 * RandomNewsCount][1] = categoryCount + 5 * RandomNewsCount+1
                arr[categoryCount + 5 * RandomNewsCount][2] = doc['title']
                arr[categoryCount + 5 * RandomNewsCount][3] = doc['description']
                arr[categoryCount + 5 * RandomNewsCount][4] = doc['url']
                RandomNewsCount += 1

        # business
        RandomNewsCount = 0
        categoryCount += 1
        for doc in dataBusiness['articles']:
            categoryName = 'business'
            if (RandomNewsCount >= 4):
                break
            if (doc['description'] != None and doc['description'] != ""):
                arr[categoryCount + 5 * RandomNewsCount][0]= categoryName
                arr[categoryCount + 5 * RandomNewsCount][1] = categoryCount + 5 * RandomNewsCount+1
                arr[categoryCount + 5 * RandomNewsCount][2] = doc['title']
                arr[categoryCount + 5 * RandomNewsCount][3] = doc['description']
                arr[categoryCount + 5 * RandomNewsCount][4] = doc['url']
                RandomNewsCount += 1

        jsonData = []
        count = 1
        for arrayobject in arr:
            jsonData.append({"Category": arrayobject[0],
                             "NewsNumber": count,
                             "title": arrayobject[2],
                             "description": arrayobject[3],
                             "url": arrayobject[4],
                             })
            count +=1
        return json.dumps(jsonData, indent=2)
        # return arr


class news_user:
    def GET(self, userName, userPassword):

        # conStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=52.211.54.45;DATABASE=AdaptiveNewsDatabase;UID=sa;PWD=cobra@123';
        # cnxn = pypyodbc.connect(conStr)

        cnxn = pypyodbc.connect(
            ("Driver={ODBC Driver 17 for SQL Server};" "Server=52.211.54.45;" "Database=AdaptiveNewsDatabase;" "uid=sa;pwd=cobra@123"))

        cursor = cnxn.cursor()

        cursor.execute('select * from [User] where UserName=' + '\''+userName +'\'' + ' and UserPassword=' + '\''+ userPassword + '\'')

        if cursor.rowcount == 0:
            return json.dumps('Unauthenticated')
        else:
            for row in cursor:
                userID=row[0]

                break
        cursor.execute('select * from UserWeights where UserID=' + str(userID))
        item = []
        weight=0.0
        categoryID=1
        arr = []
        newsCounter = 0

        if cursor.rowcount == 0:
            return json.dumps('User not assigned any wieghts')
        for row in cursor:
            item.append(row[3])
            weight = row[3]
            # Sports
            # if(categoryID == 1):
            breakPoint = 1
            weightedNewsCount = int(round(weight * 20))
            # Sports
            if (categoryID == 1):
                categoryName='sports'
                with urllib.request.urlopen("https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
                    data = json.loads(url.read().decode())
            elif (categoryID == 2):
                categoryName='entertainment'
                with urllib.request.urlopen("https://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
                    data = json.loads(url.read().decode())
            elif (categoryID == 3):
                categoryName='politics'
                with urllib.request.urlopen("https://newsapi.org/v2/top-headlines?country=us&category=politics&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
                    data = json.loads(url.read().decode())
            elif (categoryID == 4):
                categoryName='technology'
                with urllib.request.urlopen("https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
                    data = json.loads(url.read().decode())
            elif (categoryID == 5):
                categoryName='business'
                with urllib.request.urlopen("https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
                    data = json.loads(url.read().decode())


            for doc in data['articles']:
                print(doc['title'])
                if(breakPoint > weightedNewsCount or newsCounter == 20):
                    break
                # print(doc['title'])
                if(doc['description'] != None and doc['description'] != ""):
                    arr.append([])
                    arr[newsCounter].append(categoryName)
                    arr[newsCounter].append(newsCounter+1)
                    arr[newsCounter].append((doc['title']))
                    arr[newsCounter].append((doc['description']))
                    arr[newsCounter].append(doc['url'])
                    newsCounter+=1
                    breakPoint+=1
                    print(newsCounter)
            categoryID+=1
        jsonData = []
        count = 1
        for arrayobject in arr:
            jsonData.append({"Category": arrayobject[0],
                             "NewsNumber": count,
                             "title": arrayobject[2],
                             "description": arrayobject[3],
                             "url": arrayobject[4],
                             })
            count += 1
        return json.dumps(jsonData, indent=2)




class news_usermodel:
    def GET(self, userModelName):

        cnxn = pypyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" "Server=52.211.54.45;" "Database=AdaptiveNewsDatabase;" "uid=sa;pwd=cobra@123")
        cursor = cnxn.cursor()
        cursor.execute('select * from [UserModels] where UserModelName=' + '\''+userModelName +'\'')

        if cursor.rowcount == 0:
            return json.dumps('User Model doesn\'t exist')
        else:
            for row in cursor:
                userModelID=row[0]
                print(userModelID)
                break
        cursor.execute('select * from UserModelWeights where UserModelID=' + str(userModelID))
        weight=0.0
        categoryID=1
        arr = []
        newsCounter = 0
        if cursor.rowcount == 0:
            return json.dumps('Model not assigned any wieghts')
        for row in cursor:
            weight = row[3]
            breakPoint = 1
            weightedNewsCount = int(round(weight * 20))

            # Sports
            if (categoryID == 1):
                categoryName='sports'
                with urllib.request.urlopen("https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
                    data = json.loads(url.read().decode())
            elif (categoryID == 2):
                categoryName='entertainment'
                with urllib.request.urlopen("https://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
                    data = json.loads(url.read().decode())
            elif (categoryID == 3):
                categoryName='politics'
                with urllib.request.urlopen("https://newsapi.org/v2/top-headlines?country=us&category=politics&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
                    data = json.loads(url.read().decode())
            elif (categoryID == 4):
                categoryName='technology'
                with urllib.request.urlopen("https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
                    data = json.loads(url.read().decode())
            elif (categoryID == 5):
                categoryName='business'
                with urllib.request.urlopen("https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=fcd148d3e7a44031b2f7ef24590d12f8") as url:
                    data = json.loads(url.read().decode())

            for doc in data['articles']:
                if(breakPoint > weightedNewsCount or newsCounter == 20):
                    break
                # print(doc['title'])
                if (doc['description'] != None and doc['description'] != ""):

                    arr.append([])
                    arr[newsCounter].append(categoryName)
                    arr[newsCounter].append(newsCounter + 1)
                    arr[newsCounter].append(doc['title'])
                    arr[newsCounter].append(doc['description'])
                    arr[newsCounter].append(doc['url'])
                    newsCounter += 1
                    breakPoint+=1
            categoryID+=1
        jsonData = []
        count = 1
        for arrayobject in arr:
            jsonData.append({"Category": arrayobject[0],
                             "NewsNumber": count,
                             "title": arrayobject[2],
                             "description": arrayobject[3],
                             "url": arrayobject[4],
                             })
            count += 1
        return json.dumps(jsonData, indent=2)

# Learning API


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
            print(row)
            item.append(row[3])
        jsonData = []

        jsonData.append({"sports": item[0],
                         "entertainment": item[1],
                         "politics": item[2],
                         "technology": item[3],
                         "business": item[4]
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
            return json.dumps('Parameters missing')

if __name__ == "__main__":
    app.run()