from utils import Choices, check_roll
from random import random
from name_prefix_suffix import get_name
from mongo import MongoInterface
from events import log_event

discovery_types = Choices(("system", 5),
                          ("planet", 20),
                          ("asteroid", 1),
                          ("alien craft", 50),
                          ("alien planet", 100))

resource_tables = {'chance to appear':
                       {'asteroid': {'light ores': 0.75,
                                     'heavy ores': 0.1,
                                     'light gases': 0.3},
                        'system': {'light ores': 1.0,
                                   'heavy ores': 0.75,
                                   'rare ores': 0.1,
                                   'light gases': 0.7,
                                   'heavy gases': 0.4,
                                   'rare gases': 0.2,
                                   'consumables': 0.5},
                        'planet': {'light ores': 1.0,
                                   'heavy ores': 0.95,
                                   'rare ores': 0.5,
                                   'light gases': 0.2,
                                   'heavy gases': 0.2,
                                   'rare gases': 0.3,
                                   'consumables': 0.9},
                        'alien craft': {'light ores': 0.2,
                                        'heavy ores': 0.8,
                                        'rare ores': 0.7,
                                        'unique ores': 0.4,
                                        'light gases': 0.2,
                                        'heavy gases': 0.2,
                                        'rare gases': 0.6,
                                        'unique gases': 0.4},
                        'alien planet': {'light ores': 0.7,
                                         'heavy ores': 0.8,
                                         'rare ores': 0.9,
                                         'unique ores': 0.6,
                                         'light gases': 0.6,
                                         'heavy gases': 0.6,
                                         'rare gases': 0.8,
                                         'unique gases': 0.8,
                                         'consumables': 1.0}},
                   'extraction potential':
                       {'asteroid': {'light ores': 0.5,
                                     'heavy ores': 0.1,
                                     'light gases': 0.25},
                        'system': {'light ores': 0.75,
                                   'heavy ores': 0.5,
                                   'rare ores': 0.1,
                                   'light gases': 0.45,
                                   'heavy gases': 0.25,
                                   'rare gases': 0.15,
                                   'consumables': 0.35},
                        'planet': {'light ores': 0.9,
                                   'heavy ores': 0.3,
                                   'rare ores': 0.2,
                                   'light gases': 0.8,
                                   'heavy gases': 0.4,
                                   'rare gases': 0.3,
                                   'consumables': 0.9},
                        'alien craft': {'light ores': 0.8,
                                        'heavy ores': 0.7,
                                        'rare ores': 0.6,
                                        'unique ores': 0.6,
                                        'light gases': 0.8,
                                        'heavy gases': 0.7,
                                        'rare gases': 0.6,
                                        'unique gases': 0.6},
                        'alien planet': {'light ores': 0.9,
                                         'heavy ores': 0.8,
                                         'rare ores': 0.8,
                                         'unique ores': 0.8,
                                         'light gases': 0.9,
                                         'heavy gases': 0.8,
                                         'rare gases': 0.8,
                                         'unique gases': 0.8,
                                         'consumables': 0.6}}}
                   
def possibly_make_discovery(prob_of_discovery, num_exp_drones, num_discoveries):
    if num_discoveries == 0:
        num_discoveries = 1
    chance_of_disc = min( max( (prob_of_discovery * num_exp_drones) / num_discoveries, prob_of_discovery), 1.0)
    if check_roll(chance_of_disc):
        disc_type = discovery_types.random_choice()
        # TODO: get existing names
        name = get_name()#existing_names)

        resources = []
        for key, value in resource_tables['chance to appear'][disc_type].iteritems():
            # check if it appears
            if check_roll(value):
                # check for extraction potential
                potential = random() * resource_tables['extraction potential'][disc_type][key]
                resources.append((key, potential),)
        if not name:
            return None
        return {'name': name,
                'type': disc_type,
                'resources': dict(resources)}
    else:
        return None
                             
def run_discovery(mint, user):
    num_drones = mint.get_user_exploration_drones(user)
    cur_discoveries = mint.get_discoveries(user)

    disc = possibly_make_discovery(0.2, num_drones, len(cur_discoveries))
    if disc:
        cur_discoveries.append(disc)
        mint.set_discoveries(user, cur_discoveries)
        log_event(mint, user, "You have discovered a new %s named %s!" % (disc['type'], disc['name']))
        print '%s made discovery: %s' % (user, disc)

    
