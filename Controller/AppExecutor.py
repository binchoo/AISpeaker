#!/usr/bin/python
#-*- coding: utf-8 -*-
from .AppFactory import AppFactory

class AppExecutor:
    def executeApp(self, app_type, question):
        app_instance = AppFactory().initApp(app_type)
        response = app_instance.execute(question)
        return response

