(in-package :idrones)

(defun login-time-key (id)
  (concatenate 'string id ":login-time"))

(defun set-login-time (id)
  (redis:red-set (login-time-key id) (get-universal-time)))

(defun get-login-time (id)
  (redis:red-get (login-time-key id)))