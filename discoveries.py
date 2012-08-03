from utils import Choices, check_roll
from random import random
from name_prefix_suffix import get_name
from mongo import MongoInterface

discovery_types = Choices(("system", 5),
                          ("planet", 20),
                          ("asteroid", 1),
                          ("alien craft", 50),
                          ("alien planet", 100))

# TODO add the rest of the resource probs
resource_tables = {'chance to appear':
                       {'asteroid': {'light ores': 0.75,
                                     'heavy ores': 0.1,
                                     'light gases': 0.3},
                        'system': {'light ores': 1.0,
                                   'heavy ores': 0.75,
                                   'rare ores': 0.1,
                                   'light gases': 0.7,
                                   'heavy gases': 0.4,
                                   'rare gases': 0.2}},
                   'extraction potential':
                       {'asteroid': {'light ores': 0.5,
                                     'heavy ores': 0.1,
                                     'light gases': 0.25},
                        'system': {'light ores': 0.75,
                                   'heavy ores': 0.5,
                                   'rare ores': 0.1,
                                   'light gases': 0.45,
                                   'heavy gases': 0.25,
                                   'rare gases': 0.15}}}
                   
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
        print '%s made discovery: %s' % (user, disc)

    
