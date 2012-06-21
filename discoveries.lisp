(in-package :idrones-sys)

(defparameter *discovery-types*
  '(("system" . 5)
    ("planet" . 20)
    ("asteroid" . 1)
    ("alien craft" . 50)
    ("alien planet" . 100)))    

(defun possibly-make-discovery (prob-of-discovery num-exp-drones num-discoveries)
  (let ((chance-of-disc (min (max (/ (* prob-of-discovery num-exp-drones) num-discoveries)
                                  prob-of-discovery)
                             1.0)))
    (unless (check-roll chance-of-disc)
      (return-from possibly-make-discovery nil))
    (list :name (make-name)
          :type (
    