from discoveries import run_discovery
from resources import gen_resources
from mongo import MongoInterface
from datetime import datetime, timedelta
from time import sleep

if __name__ == '__main__':
    updateFreq = timedelta(seconds=1)
    nextUpdate = datetime.utcnow()
    while True:
        walltime = datetime.utcnow()

        if walltime < nextUpdate:
            sleep(1)
            continue

        print 'updating at: %s' % str(walltime)
        
        nextUpdate += updateFreq
        mint = MongoInterface()

        users = ['firestaff@gmail.com']

        for user in users:
            run_discovery(mint, user)
            gen_resources(mint, user)

        mint.close()
        
