(defpackage :idle-drones-sys
  (:nicknames :idrones-sys)
  (:use :cl))

(in-package :idrones-sys)

(defun check-roll (prob)
  (<= (random 1.0) prob))

;; choice stuff

(defstruct (choices)
  (weights)
  (cdf))

(defun make-pdf-from-choices/weights (choices)
  (let ((factors (cdr (loop with prev for c in choices collecting
                           (prog1
                               (when prev
                                 (/ (cdr c) (float prev)))
                             (setf prev (cdr c)))))))
    (labels ((rec (factors weight)
               (if (null factors)
                   (list (/ 1.0 weight))
                   (let ((pn (rec (cdr factors) (1+ (* weight (car factors))))))
                     (cons (* (car factors) (car pn)) pn)))))
      (let ((probs (rec factors 1)))
        (loop for c in choices for p in probs collecting
             (cons (car c) p))))))

(defun make-cdf-from-pdf (pdf)
  (let* ((sorted (sort pdf #'> :key #'cdr)))
    (let ((cdf-total 0))
      (loop for v in sorted collect
           (progn
             (incf cdf-total (cdr v))
             (cons (car v) cdf-total))))))

(defun random-choice (choices)
  (declare (choices choices))
  (let ((choice (random 1.0)))
    (loop for c in (choices-cdf choices) do
         (when (<= choice (cdr c))
           (return (car c))))))

(defmacro define-choice-weights (types-var choices)
  (let ((cs (gensym "choices")))
    `(let ((,cs ,choices))
       (defparameter ,types-var
         (make-choices :weights ,cs
                       :cdf (make-cdf-from-pdf 
                             (make-pdf-from-choices/weights ,cs)))))))
  