# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "vpa_host: 2 messages, 2 services")

set(MSG_I_FLAGS "-Ivpa_host:/home/student/snam_host/src/vpa_host/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(vpa_host_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/student/snam_host/src/vpa_host/msg/InterInfo.msg" NAME_WE)
add_custom_target(_vpa_host_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "vpa_host" "/home/student/snam_host/src/vpa_host/msg/InterInfo.msg" "vpa_host/RobotInfo"
)

get_filename_component(_filename "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg" NAME_WE)
add_custom_target(_vpa_host_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "vpa_host" "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg" ""
)

get_filename_component(_filename "/home/student/snam_host/src/vpa_host/srv/AssignTask.srv" NAME_WE)
add_custom_target(_vpa_host_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "vpa_host" "/home/student/snam_host/src/vpa_host/srv/AssignTask.srv" ""
)

get_filename_component(_filename "/home/student/snam_host/src/vpa_host/srv/InterMng.srv" NAME_WE)
add_custom_target(_vpa_host_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "vpa_host" "/home/student/snam_host/src/vpa_host/srv/InterMng.srv" "std_msgs/Header:vpa_host/RobotInfo"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(vpa_host
  "/home/student/snam_host/src/vpa_host/msg/InterInfo.msg"
  "${MSG_I_FLAGS}"
  "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/vpa_host
)
_generate_msg_cpp(vpa_host
  "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/vpa_host
)

### Generating Services
_generate_srv_cpp(vpa_host
  "/home/student/snam_host/src/vpa_host/srv/AssignTask.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/vpa_host
)
_generate_srv_cpp(vpa_host
  "/home/student/snam_host/src/vpa_host/srv/InterMng.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/vpa_host
)

### Generating Module File
_generate_module_cpp(vpa_host
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/vpa_host
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(vpa_host_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(vpa_host_generate_messages vpa_host_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/msg/InterInfo.msg" NAME_WE)
add_dependencies(vpa_host_generate_messages_cpp _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg" NAME_WE)
add_dependencies(vpa_host_generate_messages_cpp _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/srv/AssignTask.srv" NAME_WE)
add_dependencies(vpa_host_generate_messages_cpp _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/srv/InterMng.srv" NAME_WE)
add_dependencies(vpa_host_generate_messages_cpp _vpa_host_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(vpa_host_gencpp)
add_dependencies(vpa_host_gencpp vpa_host_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS vpa_host_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(vpa_host
  "/home/student/snam_host/src/vpa_host/msg/InterInfo.msg"
  "${MSG_I_FLAGS}"
  "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/vpa_host
)
_generate_msg_eus(vpa_host
  "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/vpa_host
)

### Generating Services
_generate_srv_eus(vpa_host
  "/home/student/snam_host/src/vpa_host/srv/AssignTask.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/vpa_host
)
_generate_srv_eus(vpa_host
  "/home/student/snam_host/src/vpa_host/srv/InterMng.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/vpa_host
)

### Generating Module File
_generate_module_eus(vpa_host
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/vpa_host
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(vpa_host_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(vpa_host_generate_messages vpa_host_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/msg/InterInfo.msg" NAME_WE)
add_dependencies(vpa_host_generate_messages_eus _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg" NAME_WE)
add_dependencies(vpa_host_generate_messages_eus _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/srv/AssignTask.srv" NAME_WE)
add_dependencies(vpa_host_generate_messages_eus _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/srv/InterMng.srv" NAME_WE)
add_dependencies(vpa_host_generate_messages_eus _vpa_host_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(vpa_host_geneus)
add_dependencies(vpa_host_geneus vpa_host_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS vpa_host_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(vpa_host
  "/home/student/snam_host/src/vpa_host/msg/InterInfo.msg"
  "${MSG_I_FLAGS}"
  "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/vpa_host
)
_generate_msg_lisp(vpa_host
  "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/vpa_host
)

### Generating Services
_generate_srv_lisp(vpa_host
  "/home/student/snam_host/src/vpa_host/srv/AssignTask.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/vpa_host
)
_generate_srv_lisp(vpa_host
  "/home/student/snam_host/src/vpa_host/srv/InterMng.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/vpa_host
)

### Generating Module File
_generate_module_lisp(vpa_host
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/vpa_host
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(vpa_host_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(vpa_host_generate_messages vpa_host_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/msg/InterInfo.msg" NAME_WE)
add_dependencies(vpa_host_generate_messages_lisp _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg" NAME_WE)
add_dependencies(vpa_host_generate_messages_lisp _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/srv/AssignTask.srv" NAME_WE)
add_dependencies(vpa_host_generate_messages_lisp _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/srv/InterMng.srv" NAME_WE)
add_dependencies(vpa_host_generate_messages_lisp _vpa_host_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(vpa_host_genlisp)
add_dependencies(vpa_host_genlisp vpa_host_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS vpa_host_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(vpa_host
  "/home/student/snam_host/src/vpa_host/msg/InterInfo.msg"
  "${MSG_I_FLAGS}"
  "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/vpa_host
)
_generate_msg_nodejs(vpa_host
  "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/vpa_host
)

### Generating Services
_generate_srv_nodejs(vpa_host
  "/home/student/snam_host/src/vpa_host/srv/AssignTask.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/vpa_host
)
_generate_srv_nodejs(vpa_host
  "/home/student/snam_host/src/vpa_host/srv/InterMng.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/vpa_host
)

### Generating Module File
_generate_module_nodejs(vpa_host
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/vpa_host
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(vpa_host_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(vpa_host_generate_messages vpa_host_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/msg/InterInfo.msg" NAME_WE)
add_dependencies(vpa_host_generate_messages_nodejs _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg" NAME_WE)
add_dependencies(vpa_host_generate_messages_nodejs _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/srv/AssignTask.srv" NAME_WE)
add_dependencies(vpa_host_generate_messages_nodejs _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/srv/InterMng.srv" NAME_WE)
add_dependencies(vpa_host_generate_messages_nodejs _vpa_host_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(vpa_host_gennodejs)
add_dependencies(vpa_host_gennodejs vpa_host_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS vpa_host_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(vpa_host
  "/home/student/snam_host/src/vpa_host/msg/InterInfo.msg"
  "${MSG_I_FLAGS}"
  "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vpa_host
)
_generate_msg_py(vpa_host
  "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vpa_host
)

### Generating Services
_generate_srv_py(vpa_host
  "/home/student/snam_host/src/vpa_host/srv/AssignTask.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vpa_host
)
_generate_srv_py(vpa_host
  "/home/student/snam_host/src/vpa_host/srv/InterMng.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vpa_host
)

### Generating Module File
_generate_module_py(vpa_host
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vpa_host
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(vpa_host_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(vpa_host_generate_messages vpa_host_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/msg/InterInfo.msg" NAME_WE)
add_dependencies(vpa_host_generate_messages_py _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/msg/RobotInfo.msg" NAME_WE)
add_dependencies(vpa_host_generate_messages_py _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/srv/AssignTask.srv" NAME_WE)
add_dependencies(vpa_host_generate_messages_py _vpa_host_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/snam_host/src/vpa_host/srv/InterMng.srv" NAME_WE)
add_dependencies(vpa_host_generate_messages_py _vpa_host_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(vpa_host_genpy)
add_dependencies(vpa_host_genpy vpa_host_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS vpa_host_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/vpa_host)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/vpa_host
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(vpa_host_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/vpa_host)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/vpa_host
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(vpa_host_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/vpa_host)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/vpa_host
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(vpa_host_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/vpa_host)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/vpa_host
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(vpa_host_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vpa_host)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vpa_host\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vpa_host
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(vpa_host_generate_messages_py std_msgs_generate_messages_py)
endif()
