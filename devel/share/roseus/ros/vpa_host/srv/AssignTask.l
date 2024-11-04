;; Auto-generated. Do not edit!


(when (boundp 'vpa_host::AssignTask)
  (if (not (find-package "VPA_HOST"))
    (make-package "VPA_HOST"))
  (shadow 'AssignTask (find-package "VPA_HOST")))
(unless (find-package "VPA_HOST::ASSIGNTASK")
  (make-package "VPA_HOST::ASSIGNTASK"))
(unless (find-package "VPA_HOST::ASSIGNTASKREQUEST")
  (make-package "VPA_HOST::ASSIGNTASKREQUEST"))
(unless (find-package "VPA_HOST::ASSIGNTASKRESPONSE")
  (make-package "VPA_HOST::ASSIGNTASKRESPONSE"))

(in-package "ROS")





(defclass vpa_host::AssignTaskRequest
  :super ros::object
  :slots (_robot_name ))

(defmethod vpa_host::AssignTaskRequest
  (:init
   (&key
    ((:robot_name __robot_name) "")
    )
   (send-super :init)
   (setq _robot_name (string __robot_name))
   self)
  (:robot_name
   (&optional __robot_name)
   (if __robot_name (setq _robot_name __robot_name)) _robot_name)
  (:serialization-length
   ()
   (+
    ;; string _robot_name
    4 (length _robot_name)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _robot_name
       (write-long (length _robot_name) s) (princ _robot_name s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _robot_name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _robot_name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass vpa_host::AssignTaskResponse
  :super ros::object
  :slots (_task_list ))

(defmethod vpa_host::AssignTaskResponse
  (:init
   (&key
    ((:task_list __task_list) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _task_list __task_list)
   self)
  (:task_list
   (&optional __task_list)
   (if __task_list (setq _task_list __task_list)) _task_list)
  (:serialization-length
   ()
   (+
    ;; int8[] _task_list
    (* 1    (length _task_list)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int8[] _task_list
     (write-long (length _task_list) s)
     (dotimes (i (length _task_list))
       (write-byte (elt _task_list i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int8[] _task_list
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _task_list (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _task_list i) (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> (elt _task_list i) 127) (setf (elt _task_list i) (- (elt _task_list i) 256)))
     ))
   ;;
   self)
  )

(defclass vpa_host::AssignTask
  :super ros::object
  :slots ())

(setf (get vpa_host::AssignTask :md5sum-) "cdad0eb519e23dd2b5d3e4c2e2b7ecf6")
(setf (get vpa_host::AssignTask :datatype-) "vpa_host/AssignTask")
(setf (get vpa_host::AssignTask :request) vpa_host::AssignTaskRequest)
(setf (get vpa_host::AssignTask :response) vpa_host::AssignTaskResponse)

(defmethod vpa_host::AssignTaskRequest
  (:response () (instance vpa_host::AssignTaskResponse :init)))

(setf (get vpa_host::AssignTaskRequest :md5sum-) "cdad0eb519e23dd2b5d3e4c2e2b7ecf6")
(setf (get vpa_host::AssignTaskRequest :datatype-) "vpa_host/AssignTaskRequest")
(setf (get vpa_host::AssignTaskRequest :definition-)
      "string robot_name
---
int8[] task_list
")

(setf (get vpa_host::AssignTaskResponse :md5sum-) "cdad0eb519e23dd2b5d3e4c2e2b7ecf6")
(setf (get vpa_host::AssignTaskResponse :datatype-) "vpa_host/AssignTaskResponse")
(setf (get vpa_host::AssignTaskResponse :definition-)
      "string robot_name
---
int8[] task_list
")



(provide :vpa_host/AssignTask "cdad0eb519e23dd2b5d3e4c2e2b7ecf6")


