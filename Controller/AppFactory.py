import Application as Apps


class AppFactory():

    _app_list = {
        'news': 'NewsApplication',
        'weather': 'WeatherApplication',
        'stock': 'StockApplication',
        'bible': 'BibleApplication',
    }

    @staticmethod
    def initApp(app_type):

        if AppFactory._has_application(app_type):
            app_class_name = AppFactory._app_list[app_type]
            app_class = getattr(Apps, app_class_name)
            app_instance = app_class()
        else:
            print('app_type {} is not a application'.format(app_type))
            raise Exception
        return app_instance

    @staticmethod
    def _has_application(app_type):
        return app_type in AppFactory._app_list.keys()

    @staticmethod
    def append_app_list(app_type, app_name):

        if AppFactory._has_application(app_type):
            print('app_type {} is already in use.'.format(app_type))
            raise Exception
        else:
            AppFactory._app_list[app_type] = app_name
