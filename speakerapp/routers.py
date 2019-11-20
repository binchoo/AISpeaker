class MultiDBRouter(object):
    def __init__(self):
        self.app_label = ['chart', 'bible', 'default']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.app_label:
            return model._meta.app_label

        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.app_label:
            return model._meta.app_label

        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.app_label or \
                obj2._meta.app_label in self.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.app_label:
            return db in self.app_label
        elif db == 'default':
            return True

        return None