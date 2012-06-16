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
               "drakma"
               "cl-json"
               "chillax")
  :components
  ((:file "package")
   (:file "couch")
   (:file "main"))
  :serial t)