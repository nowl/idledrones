(in-package :idrones-sys)

(define-choice-weights *discovery-types*
  '(("system" . 5)
    ("planet" . 20)
    ("asteroid" . 1)
    ("alien craft" . 50)
    ("alien planet" . 100)))

;; (chance of appearing) (extraction potential)
(defparameter *resource-table*
  '(("asteroid" . (("light ores"  0.75 0.5)
                   ("heavy ores"  0.1  0.1)
                   ("light gases" 0.3  0.25)))
    ("system" . (("light ores"  1.0 0.75)
                 ("heavy ores"  0.75  0.5)
                 ("rare ores"  0.1  0.1)
                 ("light gases" 0.7  0.45)
                 ("heavy gases" 0.4  0.25)
                 ("rare gases" 0.2  0.15)))))
  
(defun possibly-make-discovery (prob-of-discovery num-exp-drones num-discoveries)
  (let ((chance-of-disc (min (max (/ (* prob-of-discovery num-exp-drones) num-discoveries)
                                  prob-of-discovery)
                             1.0)))
    (unless (check-roll chance-of-disc)
      (return-from possibly-make-discovery nil))
    (let ((type (random-choice *discovery-types*)))
      (list :name (make-name)
            :type type
            :resources (remove-if #'null
                                  (loop for resource in (cdr (assoc type *resource-table* :test #'equal)) collecting
                                       (destructuring-bind (res-type appear-prob extract-prob) resource
                                         (if (check-roll appear-prob)
                                             (cons res-type (random extract-prob))))))))))
            
                             
                         
          
    