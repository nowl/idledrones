from utils import Choices, check_roll
from naming import read_from_file, random_word
from mongo import MongoInterface

discovery_types = Choices(("system", 5),
                          ("planet", 20),
                          ("asteroid", 1),
                          ("alien craft", 50),
                          ("alien planet", 100))

name_cdf = read_from_file('planet-name.cdf')

mint = MongoInterface()

# ;; (chance of appearing) (extraction potential)
# (defparameter *resource-table*
#   '(("asteroid" . (("light ores"  0.75 0.5)
#                    ("heavy ores"  0.1  0.1)
#                    ("light gases" 0.3  0.25)))
#     ("system" . (("light ores"  1.0 0.75)
#                  ("heavy ores"  0.75  0.5)
#                  ("rare ores"  0.1  0.1)
#                  ("light gases" 0.7  0.45)
#                  ("heavy gases" 0.4  0.25)
#                  ("rare gases" 0.2  0.15)))))

def possibly_make_discovery(prob_of_discovery, num_exp_drones, num_discoveries):
    chance_of_disc = min( max( (prob_of_discovery * num_exp_drones) / num_discoveries, prob_of_discovery), 1.0)
    if check_roll(chance_of_disc):
        disc_type = discovery_types.random_choice()
        name = random_word(name_cdf, min=4, max=10)
        return {'name': name, 'type': disc_type}
    else:
        return None

for i in range(100):
    user = 'firestaff@gmail.com'
    disc = possibly_make_discovery(0.2, 10, 20)
    if disc:
        cur_discoveries = mint.get_discoveries(user)
        cur_discoveries.append(disc)
        mint.set_discoveries(user, cur_discoveries)
        print '%s made discovery: %s' % (user, disc)
  
# (defun possibly-make-discovery (prob-of-discovery num-exp-drones num-discoveries)
#   (let ((chance-of-disc (min (max (/ (* prob-of-discovery num-exp-drones) num-discoveries)
#                                   prob-of-discovery)
#                              1.0)))
#     (unless (check-roll chance-of-disc)
#       (return-from possibly-make-discovery nil))
#     (let ((type (random-choice *discovery-types*)))
#       (list :name (make-name)
#             :type type
#             :resources (remove-if #'null
#                                   (loop for resource in (cdr (assoc type *resource-table* :test #'equal)) collecting
#                                        (destructuring-bind (res-type appear-prob extract-prob) resource
#                                          (if (check-roll appear-prob)
#                                              (cons res-type (random extract-prob))))))))))
            
                             
mint.close()
