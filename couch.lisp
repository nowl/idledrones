(in-package :idrones)

(defparameter *couch-server* (make-instance 'chillax:yason-server :object-as-alist-p t
                                            :parse-object-key-fun
                                            (lambda (string) (intern string *package*))))

(defparameter *couch-db* (chillax:ensure-db *couch-server* "idle-drones"))

(defmacro with-gensyms ((&rest syms) &body body)
  `(let ,(loop for sym in syms collect
              `(,sym (gensym)))
     ,@body))

(defmacro get-from-document (id name)
  (with-gensyms (n doc value)
    `(let* ((,n ,name)
            (,doc (chillax:get-document *couch-db* ,id :errorp nil))
            (,value (assoc (etypecase ,n
                             (symbol ,n)
                             (string (intern ,n)))
                           ,doc)))
       (if ,value
           (read-from-string (cdr ,value))))))

(defmacro set-in-document (id name value)
  (with-gensyms (n doc)
    `(let* ((,n ,name)
            (,n (etypecase ,n
                  (symbol ,n)
                  (string (intern ,n))))
            (,doc (delete ,n (chillax:get-document *couch-db* ,id :errorp nil) :key #'car)))
       (pushnew (cons ,n (format nil "~a" ,value)) ,doc :key #'car)
       (format t "~a" ,doc)
       (chillax:put-document *couch-db* ,id ,doc))))

(defun set-login-time (id) (set-in-document id "last-login-time" (get-universal-time)))
(defun get-login-time (id) (get-from-document id "last-login-time"))

(defun add-discovery (id discovery)
  (let ((discoveries (get-from-document id "discoveries")))
    (set-in-document id "discoveries" (cons discovery discoveries))))
(defun remove-discovery (id discovery)
  (let ((discoveries (get-from-document id "discoveries")))
    (set-in-document id "discoveries" (delete discovery discoveries :test #'equal))))
(defun get-discoveries (id)
  (get-from-document id "discoveries"))