(defmacro tl-run (&body body)
  `(eval-when (:compile-toplevel :load-toplevel :execute)
     ,@body))

(tl-run (load "~/quicklisp/setup.lisp"))
(tl-run (ql:quickload :hunchentoot))
(tl-run (ql:quickload :parenscript))
(tl-run (ql:quickload :html-template))
(tl-run (ql:quickload :cl-json))
(eval-when (:compile-toplevel)
  (unless (find-package :custom-json)
    (rename-package :json :custom-json)))
(tl-run (ql:quickload :drakma))
;(tl-run (ql:quickload :chillax))
(tl-run (ql:quickload :yason))
(tl-run
  (pushnew #p"/home/nowl/dev/chillax/" asdf:*central-registry*)
  (require 'chillax))
(tl-run (require 'idledrones))
(tl-run (require 'idledrones-sys))