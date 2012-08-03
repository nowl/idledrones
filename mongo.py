from pymongo import Connection
import datetime
from functools import wraps
        
def fail_safe(typ):
    def fail_safe_f(f):
        @wraps(f)
        def decorator(*args, **kwds):
            try:
                return f(*args, **kwds)
            except:
                return typ
        return decorator
    return fail_safe_f

class MongoInterface ():
    def __init__(self,
                 server = 'localhost',
                 port = 27017,
                 db_name = 'idledrones',
                 collection = 'collection1'):
        self.connection = Connection(server, port)
        self.db = self.connection[db_name]
        self.collection = self.db[collection]

    def close(self):
        try:
            self.connection.close()
        except:
            pass
    
    def _get(self, spec):
        return self.collection.find_one(spec)

    def _set(self, spec, field, value):
        old = self._get(spec)
        if old:
            self.collection.update(spec, {'$set': {field: value}})
        else:
            spec[field] = value
            self.collection.insert(spec)

    def set_login_time(self, user):        
        self._set({'user': user,
                   'type': 'user_info'},
                  'last-login-time',
                  datetime.datetime.utcnow())
    
    @fail_safe(None)
    def get_login_time(self, user):
        return self._get({'user': user, 'type': 'user_info'})['last-login-time']

    def set_discoveries(self, user, discoveries):
        self._set({'user': user,
                   'type': 'user_info'},
                  'discoveries',
                  repr(discoveries))

    @fail_safe([])
    def get_discoveries(self, user):
        return eval(self._get({'user': user, 'type': 'user_info'})['discoveries'])

    def set_user_exploration_drones(self, user, num_drones):
        self._set({'user': user,
                   'type': 'user_info'},
                  'exploration drones',
                  num_drones)

    @fail_safe(0)
    def get_user_exploration_drones(self, user):
        return self._get({'user': user, 'type': 'user_info'})['exploration drones']


if __name__ == '__main__':
    mint = MongoInterface()
    #mint.set_login_time('firestaff@gmail.com')
    #print mint.get_login_time('firestaff@gmail.com')
    #mint.get_discoveries('firestaff@gmail.com')
    #mint.set_discoveries('firestaff@gmail.com',
    #                     [{'name': 'name 1', 'type': 'asteroid'},
    #                      {'name': 'name 2', 'type': 'system'},
    #                      {'name': 'name 3', 'type': 'alien craft'},])
