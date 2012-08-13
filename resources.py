from events import log_event
from collections import defaultdict

BASE_EXTRACTION = 10

def update_resources(disc, res):
    for typ, pot in disc.iteritems():
        res[typ] += BASE_EXTRACTION * pot

def gen_resources(mint, user):
    discoveries = mint.get_discoveries(user)
    
    new_resources = defaultdict(lambda: 0)
    for disc in discoveries:
        update_resources(disc['resources'], new_resources)
        
    resources = mint.get_resources(user)
    new = {}
    types = ['light ores', 'heavy ores', 'rare ores', 'unique ores',
             'light gases', 'heavy gases', 'rare gases', 'unique gases',
             'consumables']
    for typ in types:
        new[typ] = resources.get(typ, 0) + int(new_resources[typ])

        if new_resources[typ] != 0:
            log_event(mint, user, "Your drones have extracted %d %s." % (new_resources[typ], typ))

    mint.set_resources(user, new)
    return new
