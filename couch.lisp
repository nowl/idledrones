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
  (with-gensyms (n doc)
    `(let* ((,n ,name)
            (,doc (chillax:get-document *couch-db* ,id :errorp nil)))
       (assoc (etypecase ,n
                (symbol ,n)
                (string (intern ,n)))
              ,doc))))

(defmacro set-in-document (id name value)
  (with-gensyms (n doc)
    `(let* ((,n ,name)
            (,n (etypecase ,n
                  (symbol ,n)
                  (string (intern ,n))))
            (,doc (delete ,n (chillax:get-document *couch-db* ,id :errorp nil) :key #'car)))
       (pushnew (cons ,n ,value) ,doc :key #'car)
       (chillax:put-document *couch-db* ,id ,doc))))

(defmacro add-in-list-document (id name value)
  (with-gensyms (n doc doc*)
    `(let* ((,n ,name)
            (,n (etypecase ,n
                  (symbol ,n)
                  (string (intern ,n))))
            (,doc (chillax:get-document *couch-db* ,id :errorp nil))
            (,doc* (assoc ,n ,doc)))
       (if ,doc*
           (rplacd ,doc* (cons ,value (cdr ,doc*)))
           (push (cons ,n (list ,value)) ,doc))
       (chillax:put-document *couch-db* ,id ,doc))))

(defmacro remove-from-list-document (id name value)
  (with-gensyms (n doc doc*)
    `(let* ((,n ,name)
            (,n (etypecase ,n
                  (symbol ,n)
                  (string (intern ,n))))
            (,doc (chillax:get-document *couch-db* ,id :errorp nil))
            (,doc* (assoc ,n ,doc)))
       (when ,doc*
         (rplacd ,doc* (delete ,value (cdr ,doc*) :test #'equal))
         (chillax:put-document *couch-db* ,id ,doc)))))

(defun set-login-time (id) (set-in-document id "last-login-time" (get-universal-time)))
(defun get-login-time (id) (get-from-document id "last-login-time"))

(defun add-discovery (id discovery)
  (add-in-list-document id "discoveries" discovery))
(defun remove-discovery (id discovery)
  (remove-from-list-document id "discoveries" discovery))