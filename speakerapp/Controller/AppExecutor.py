#!/usr/bin/python
# -*- coding: utf-8 -*-
import AppFactory as factory


class AppExecutor:
    _appDictionary = dict()

    def __init__(self):
        pass

    def findApp(self, type):
        if(type not in self._appDictionary):
            self._appDictionary[type] = self.createApp(type)
        return self._appDictionary[type]

    def createApp(self, appName):
        return factory.initApp(appName)

    def ExecuteApp(self, type, question):
        return self.findApp(type).execute(question)
