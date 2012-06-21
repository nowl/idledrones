(in-package :idrones-sys)

(defun read-names (filename)
  (with-open-file (in filename)
    (loop with names while t do
         (let ((line (read-line in nil :eof)))
           (when (eq line :eof)
             (return names))
           (push line names)))))

(defparameter *names* nil)
(defparameter *naming-stats* (make-hash-table))
(defparameter *cdf* nil)

(defun fill-stats-for-string (name)
  (declare (string name))
  (loop with last for char across name do
       (let ((lower (char-downcase char)))
         (when last
           (progn
             (when (null (gethash last *naming-stats*))
               (setf (gethash last *naming-stats*)
                     (make-hash-table)))
             (if (gethash lower (gethash last *naming-stats*))
                 (incf (gethash lower (gethash last *naming-stats*)))
                 (setf (gethash lower (gethash last *naming-stats*)) 1))))
         (setf last lower))))
                     
(defun fill-stats (names)
  (loop for name in names do
       (fill-stats-for-string name)))

;;(fill-stats *names*)

(defun get-total (hashtable)
  (let ((total 0))
    (loop for key being the hash-keys of hashtable using (hash-value value) do
         (incf total value))
    total))

(defun build-cdf (hashtable)
  (let* ((total (get-total hashtable))
         (vals (loop for key being the hash-keys of hashtable using (hash-value value) collect
                    (cons key (/ (float value) total))))
         (sorted (sort vals #'> :key #'cdr)))
    (let ((cdf-total 0))
      (loop for v in sorted collect
           (progn
             (incf cdf-total (cdr v))
             (cons (car v) cdf-total))))))

(defun build-flat-cdf ()
  (setf *cdf*
        (loop for key being the hash-keys of *naming-stats* using (hash-value value) collect
             (cons key (build-cdf value)))))

(defun read-from-corpus (filename)
  (read-names filename)
  (fill-stats *names*)
  (build-flat-cdf))

(defun read-from-existing-cdf (filename)
  (with-open-file (in filename)
    (setf *cdf* (read in))))

(read-from-existing-cdf "planet-name.cdf")

(defun find-random-next (char)
  (let ((cdf (cdr (assoc char *cdf*)))
        (rand (random 1.0)))
    (loop for prob in cdf do
         (when (< rand (cdr prob))
           (return (car prob))))))

(defun build-name (len)
  (let* ((char (car (nth (random (length *cdf*)) *cdf*)))
         (str (string char)))
    (loop for i below (1- len) do
         (let ((next (find-random-next char)))
           (setf str (concatenate 'string str (string next)))
           (setf char next)))
    str))
         
(defun make-name ()
  (build-name (+ 4 (random 6))))