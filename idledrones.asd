;;; -*- lisp -*-

(defsystem idledrones
  :description "IDLE DRONES"
  :long-description ""
  :version "0.1"
  :author "John Process <esologic@gmail.com>"
  :licence "GNU Public License"
  :depends-on ("hunchentoot"
               "parenscript"
               "html-template"
               "cl-redis"
               "cl-json"
               "drakma")
  :components
  ((:file "package")
   (:file "redis")
   (:file "main"))
  :serial t)