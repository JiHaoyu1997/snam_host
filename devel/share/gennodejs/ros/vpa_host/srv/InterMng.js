// Auto-generated. Do not edit!

// (in-package vpa_host.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let RobotInfo = require('../msg/RobotInfo.js');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------


//-----------------------------------------------------------

class InterMngRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.robot_name = null;
      this.last_inter_id = null;
      this.curr_inter_id = null;
      this.robot_info = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('robot_name')) {
        this.robot_name = initObj.robot_name
      }
      else {
        this.robot_name = '';
      }
      if (initObj.hasOwnProperty('last_inter_id')) {
        this.last_inter_id = initObj.last_inter_id
      }
      else {
        this.last_inter_id = 0;
      }
      if (initObj.hasOwnProperty('curr_inter_id')) {
        this.curr_inter_id = initObj.curr_inter_id
      }
      else {
        this.curr_inter_id = 0;
      }
      if (initObj.hasOwnProperty('robot_info')) {
        this.robot_info = initObj.robot_info
      }
      else {
        this.robot_info = new RobotInfo();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type InterMngRequest
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [robot_name]
    bufferOffset = _serializer.string(obj.robot_name, buffer, bufferOffset);
    // Serialize message field [last_inter_id]
    bufferOffset = _serializer.int8(obj.last_inter_id, buffer, bufferOffset);
    // Serialize message field [curr_inter_id]
    bufferOffset = _serializer.int8(obj.curr_inter_id, buffer, bufferOffset);
    // Serialize message field [robot_info]
    bufferOffset = RobotInfo.serialize(obj.robot_info, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type InterMngRequest
    let len;
    let data = new InterMngRequest(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [robot_name]
    data.robot_name = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [last_inter_id]
    data.last_inter_id = _deserializer.int8(buffer, bufferOffset);
    // Deserialize message field [curr_inter_id]
    data.curr_inter_id = _deserializer.int8(buffer, bufferOffset);
    // Deserialize message field [robot_info]
    data.robot_info = RobotInfo.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += _getByteLength(object.robot_name);
    length += RobotInfo.getMessageSize(object.robot_info);
    return length + 6;
  }

  static datatype() {
    // Returns string type for a service object
    return 'vpa_host/InterMngRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'a208d5c3825c6fd4cc3a482be9ed4727';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    std_msgs/Header header
    string robot_name
    int8 last_inter_id
    int8 curr_inter_id
    RobotInfo robot_info
    
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    string frame_id
    
    ================================================================================
    MSG: vpa_host/RobotInfo
    string  robot_name
    int8    robot_id
    float32 robot_a  # Acceleration
    float32 robot_v  # Velocity
    float32 robot_p  # Position
    float32 robot_enter_time
    float32 robot_arrive_cp_time
    float32 robot_exit_time
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new InterMngRequest(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.robot_name !== undefined) {
      resolved.robot_name = msg.robot_name;
    }
    else {
      resolved.robot_name = ''
    }

    if (msg.last_inter_id !== undefined) {
      resolved.last_inter_id = msg.last_inter_id;
    }
    else {
      resolved.last_inter_id = 0
    }

    if (msg.curr_inter_id !== undefined) {
      resolved.curr_inter_id = msg.curr_inter_id;
    }
    else {
      resolved.curr_inter_id = 0
    }

    if (msg.robot_info !== undefined) {
      resolved.robot_info = RobotInfo.Resolve(msg.robot_info)
    }
    else {
      resolved.robot_info = new RobotInfo()
    }

    return resolved;
    }
};

class InterMngResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.success = null;
      this.message = null;
    }
    else {
      if (initObj.hasOwnProperty('success')) {
        this.success = initObj.success
      }
      else {
        this.success = false;
      }
      if (initObj.hasOwnProperty('message')) {
        this.message = initObj.message
      }
      else {
        this.message = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type InterMngResponse
    // Serialize message field [success]
    bufferOffset = _serializer.bool(obj.success, buffer, bufferOffset);
    // Serialize message field [message]
    bufferOffset = _serializer.string(obj.message, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type InterMngResponse
    let len;
    let data = new InterMngResponse(null);
    // Deserialize message field [success]
    data.success = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [message]
    data.message = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.message);
    return length + 5;
  }

  static datatype() {
    // Returns string type for a service object
    return 'vpa_host/InterMngResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '937c9679a518e3a18d831e57125ea522';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool success
    string message
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new InterMngResponse(null);
    if (msg.success !== undefined) {
      resolved.success = msg.success;
    }
    else {
      resolved.success = false
    }

    if (msg.message !== undefined) {
      resolved.message = msg.message;
    }
    else {
      resolved.message = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: InterMngRequest,
  Response: InterMngResponse,
  md5sum() { return '6a2d2bfc797d5c6e5fd765f81f56acfb'; },
  datatype() { return 'vpa_host/InterMng'; }
};
