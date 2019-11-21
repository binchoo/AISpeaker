from . import Application as Apps

class AppFactory():

    _app_list = { 
        'news' : 'NewsApplication', 
        'weather' : 'WeatherApplication', 
        'stock' : 'StockApplication', 
        'bible': 'BibleApplication', 
    }

    def initApp(self, app_type):

        app_class_name = self._app_list[app_type]
        app_class = getattr(Apps, app_class_name)
        app_instance = app_class()
        return app_instance

    @staticmethod
    def append_app_list(app_type, app_name) :

        if app_type in AppFactory._app_list.keys() :
            print('app_type {} is already in use.'.format(app_type))
            raise Exception
        else :
            AppFactory._app_list[app_type] = app_name


    

        

