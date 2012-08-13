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

    # server level commands

    def set_users(self, users):        
        self._set({'type': 'server_info'},
                  'users',
                  repr(users))
    
    @fail_safe([])
    def get_users(self):
        return eval(self._get({'type': 'server_info'})['users'])

    def set_trades(self, trades):        
        self._set({'type': 'server_info'},
                  'trades',
                  repr(trades))
    
    @fail_safe({})
    def get_trades(self):
        return eval(self._get({'type': 'server_info'})['trades'])

    # user level commands

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

    def set_events(self, user, events):
        self._set({'user': user,
                   'type': 'user_info'},
                  'events',
                  repr(events))

    @fail_safe([])
    def get_events(self, user):
        return eval(self._get({'user': user, 'type': 'user_info'})['events'])

    def set_resources(self, user, resources):
        self._set({'user': user,
                   'type': 'user_info'},
                  'resources',
                  repr(resources))

    @fail_safe({})
    def get_resources(self, user):
        return eval(self._get({'user': user, 'type': 'user_info'})['resources'])

    def set_credits(self, user, cdits):
        self._set({'user': user,
                   'type': 'user_info'},
                  'credits',
                  cdits)

    @fail_safe(0)
    def get_credits(self, user):
        return eval(self._get({'user': user, 'type': 'user_info'})['credits'])
        


if __name__ == '__main__':
    mint = MongoInterface()
    #mint.set_login_time('firestaff@gmail.com')
    #print mint.get_login_time('firestaff@gmail.com')
    #mint.get_discoveries('firestaff@gmail.com')
    #mint.set_discoveries('firestaff@gmail.com',
    #                     [{'name': 'name 1', 'type': 'asteroid'},
    #                      {'name': 'name 2', 'type': 'system'},
    #                      {'name': 'name 3', 'type': 'alien craft'},])
