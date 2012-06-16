(in-package :idrones)

(defparameter *couch-server* (make-instance 'chillax:yason-server :object-as-alist-p t
                                            :parse-object-key-fun
                                            (lambda (string) (intern string *package*))))

(defparameter *couch-db* (chillax:ensure-db *couch-server* "hello-world"))

(defun set-login-time (id)
  (let* ((doc (chillax:get-document *couch-db* id :errorp nil))
         (doc* (pushnew (cons '|login-time| (get-universal-time))
                        doc :key #'car)))
    (chillax:put-document *couch-db* id doc*)))

(defun get-login-time (id)
  (let ((doc (chillax:get-document *couch-db* id :errorp nil)))
    (assoc '|login-time| doc)))