from discoveries import run_discovery
from resources import gen_resources
from mongo import MongoInterface
from datetime import datetime, timedelta
from time import sleep
from collections import defaultdict

trades = defaultdict(lambda: 0)

def reset_trades():
    for key in trades:
        trades[key] = 0

def append_trades(res):
    for k,v in res.iteritems():
        trades[k] += v

def calc_trades(mint):
    factors = {'light ores': 1,
               'heavy ores': 5,
               'rare ores': 10,
               'unique ores': 20,
               'light gases': 1,
               'heavy gases': 5,
               'rare gases': 10,
               'unique gases': 20,
               'consumables': 1}
    final = {}
    for k,v in trades.iteritems():
        final[k] = v * factors[k]

    mint.set_trades(final)

if __name__ == '__main__':
    # TODO: testing
    mint = MongoInterface()
    mint.set_users(['firestaff@gmail.com'])
    mint.close()

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

        reset_trades()

        users = mint.get_users()

        for user in users:
            run_discovery(mint, user)
            resources = gen_resources(mint, user)
            append_trades(resources)

        calc_trades(mint)

        mint.close()
        
