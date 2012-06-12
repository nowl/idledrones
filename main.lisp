(in-package :idrones)

(defun ensure-redis ()
  (when (not (redis:connected-p))
    (redis:connect)))

(defparameter *acceptor* (make-instance 'easy-acceptor :port 4242))

(setf (acceptor-document-root *acceptor*) #p"/home/nowl/dev/idledrones/www/")

(start *acceptor*)

(define-easy-handler (say-yo :uri "/yo") (name)
  (setf (content-type*) "text/html")
  (with-output-to-string (stream)
    (let ((*string-modifier* #'identity))
      (fill-and-print-template #p"foo.html" (list :name (escape-string-iso-8859-1 name)
                                                  :js (ps (alert "hello there")))
                               :stream stream))))

(define-easy-handler (login-url :uri "/login") ()
  (setf (content-type*) "text")
  ;; make sure we're connected to redis
  (ensure-redis)
  (let* ((local-server "http://localhost:4242")
         (verify-result-from-server
          (drakma:http-request "https://browserid.org/verify" 
                               :method :post
                               :parameters (list (cons "assertion" (post-parameter "assertion"))
                                                 (cons "audience" local-server))))
         (verify-result
          (json:decode-json-from-string (flex:octets-to-string verify-result-from-server))))
    (with-output-to-string (stream)
      (format stream "~a" verify-result))))