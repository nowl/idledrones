(in-package :idrones)

(defun ensure-redis ()
  (when (not (redis:connected-p))
    (redis:connect)))

(defparameter *local-server* "http://localhost:4242")
(defparameter *acceptor* (make-instance 'easy-acceptor :port 4242))

(setf (acceptor-document-root *acceptor*) #p"/home/nowl/dev/idledrones/www/")

(start *acceptor*)

(define-easy-handler (index :uri "/") ()
  (setf (content-type*) "text/html")
  (ensure-redis)
  (let ((id (session-value :id)))    
    (when id (set-login-time id))
    (with-output-to-string (stream)
      (fill-and-print-template #p"index.html" (list :id id)
                               :stream stream))))

(defun valid-browserid-responsep (json-result)
  (and (equal "okay" (cdr (assoc :status json-result)))
       (equal *local-server* (cdr (assoc :audience *test*)))))

(define-easy-handler (login-url :uri "/login") ()
  (setf (content-type*) "text")
  (let* ((verify-result-from-server
          (drakma:http-request "https://browserid.org/verify" 
                               :method :post
                               :parameters (list (cons "assertion" (post-parameter "assertion"))
                                                 (cons "audience" *local-server*))))
         (verify-result
          (json:decode-json-from-string (flex:octets-to-string verify-result-from-server))))
    (when (valid-browserid-responsep verify-result)
      (start-session)
      (setf (session-value :id)
            (cdr (assoc :email verify-result))))
    (with-output-to-string (stream)
      (format stream "~a" verify-result))))

(define-easy-handler (logout-url :uri "/logout") ()
  (setf (content-type*) "text/html")
  (when *session*
    (remove-session *session*))
  (redirect "/"))