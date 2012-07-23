from pymongo import Connection
import datetime
        
class MongoInterface ():
    def __init__(self,
                 server = 'localhost',
                 port = 27017,
                 db_name = 'idledrones',
                 collection = 'collection1'):
        self.connection = Connection(server, port)
        self.db = self.connection[db_name]
        self.collection = self.db[collection]
    
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
                   'type': 'login-time'},
                  'last-login-time',
                  datetime.datetime.utcnow())
    
    def get_login_time(self, user):
        return self._get({'user': user, 'type': 'login-time'})


if __name__ == '__main__':
    mint = MongoInterface()
    mint.set_login_time('firestaff@gmail.com')
    print mint.get_login_time('firestaff@gmail.com')
