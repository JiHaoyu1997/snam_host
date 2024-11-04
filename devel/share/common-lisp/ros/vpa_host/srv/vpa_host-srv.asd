
(cl:in-package :asdf)

(defsystem "vpa_host-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
               :vpa_host-msg
)
  :components ((:file "_package")
    (:file "AssignTask" :depends-on ("_package_AssignTask"))
    (:file "_package_AssignTask" :depends-on ("_package"))
    (:file "InterMng" :depends-on ("_package_InterMng"))
    (:file "_package_InterMng" :depends-on ("_package"))
  ))