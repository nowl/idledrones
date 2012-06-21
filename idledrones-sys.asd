;;; -*- lisp -*-

(defsystem idledrones-sys
  :description "IDLE DRONES System"
  :long-description ""
  :version "0.1"
  :author "John Process <esologic@gmail.com>"
  :licence "GNU Public License"
  :depends-on ("chillax")
  :components
  ((:file "utils")
   (:file "naming")
   (:file "discoveries"))
  :serial t)