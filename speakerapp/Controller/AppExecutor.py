#!/usr/bin/python
# -*- coding: utf-8 -*-
# import AppFactory as factory


class AppExecutor:
    __appDictionary = dict()

    def __init__(self):
        pass

    def ExecuteApp(self, type, question):

        return __findApp(type).execute(question)

    def __findApp(self, type):

        if(type not in __appDictionary):
            __appDictionary[type] = __createApp(type)

        return __appDictionary[type]

    def __createApp(self, appName):
        return app(appName)
        # factory.initApp(appName)


class app:
    type

    def __init__(self, type):
        this.type = type

    def execute(self, text):
        print(type + " : "+text)
