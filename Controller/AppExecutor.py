#!/usr/bin/python
# -*- coding: utf-8 -*-


class AppExecutor:

    _app_factory = AppFactory()

    def executeApp(self, app_type, question):

        self.app_instance = self._app_factory.initApp(app_type)
        response = self.app_instance.execute(question)
        return response
