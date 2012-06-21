(defpackage :idle-drones-sys
  (:nicknames :idrones-sys)
  (:use :cl))

(in-package :idrones-sys)

(defun check-roll (prob)
  (<= (random 1.0) prob))

(defun make-cdf-from-choices/weights (choices)
  (let* ((total (loop for choice in choices summing (cdr choice)))
         (inv-totals (loop for choice in choices collecting (cons (car choice)
                                                                  (- total (cdr choice)))))
         (inv-totals-sum (loop for choice in inv-totals summing (cdr choice)))
         (probs (loop for choice in inv-totals collecting (cons (car choice)
                                                                (/ (float (cdr choice)) inv-totals-sum)))))
    inv-totals))
    

(defun choice-with-weights (choices)
  "choices should be of the format ((choice1 . weight1) (choice2
. weight2) etc.)"
  