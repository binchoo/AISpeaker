import Application

class AppFactory():

    _app_module = __import__('Application')
    _app_list = { 
        'news' : 'NewsApplication', 
        'weather' : 'WeatherApplication', 
        'stock' : 'StockApplication', 
        'bible': 'BibleApplication', 
    }

    def initApp(self, app_type):
        app_class_name = AppFactory._app_list[app_type]
        app_class = getattr(AppFactory._app_module, app_class_name)
        app_instance = app_class()
        return app_instance

    def _append_app_list(self, app_type, app_name) :
        if app_type in AppFactory._app_list.keys() :
            print('app_type {} is already in use'.format(app_type))
            raise Exception
        else :
            AppFactory._app_list[app_type] = app_name


    

        

