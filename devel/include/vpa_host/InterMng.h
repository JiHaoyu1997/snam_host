// Generated by gencpp from file vpa_host/InterMng.msg
// DO NOT EDIT!


#ifndef VPA_HOST_MESSAGE_INTERMNG_H
#define VPA_HOST_MESSAGE_INTERMNG_H

#include <ros/service_traits.h>


#include <vpa_host/InterMngRequest.h>
#include <vpa_host/InterMngResponse.h>


namespace vpa_host
{

struct InterMng
{

typedef InterMngRequest Request;
typedef InterMngResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct InterMng
} // namespace vpa_host


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::vpa_host::InterMng > {
  static const char* value()
  {
    return "6a2d2bfc797d5c6e5fd765f81f56acfb";
  }

  static const char* value(const ::vpa_host::InterMng&) { return value(); }
};

template<>
struct DataType< ::vpa_host::InterMng > {
  static const char* value()
  {
    return "vpa_host/InterMng";
  }

  static const char* value(const ::vpa_host::InterMng&) { return value(); }
};


// service_traits::MD5Sum< ::vpa_host::InterMngRequest> should match
// service_traits::MD5Sum< ::vpa_host::InterMng >
template<>
struct MD5Sum< ::vpa_host::InterMngRequest>
{
  static const char* value()
  {
    return MD5Sum< ::vpa_host::InterMng >::value();
  }
  static const char* value(const ::vpa_host::InterMngRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::vpa_host::InterMngRequest> should match
// service_traits::DataType< ::vpa_host::InterMng >
template<>
struct DataType< ::vpa_host::InterMngRequest>
{
  static const char* value()
  {
    return DataType< ::vpa_host::InterMng >::value();
  }
  static const char* value(const ::vpa_host::InterMngRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::vpa_host::InterMngResponse> should match
// service_traits::MD5Sum< ::vpa_host::InterMng >
template<>
struct MD5Sum< ::vpa_host::InterMngResponse>
{
  static const char* value()
  {
    return MD5Sum< ::vpa_host::InterMng >::value();
  }
  static const char* value(const ::vpa_host::InterMngResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::vpa_host::InterMngResponse> should match
// service_traits::DataType< ::vpa_host::InterMng >
template<>
struct DataType< ::vpa_host::InterMngResponse>
{
  static const char* value()
  {
    return DataType< ::vpa_host::InterMng >::value();
  }
  static const char* value(const ::vpa_host::InterMngResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // VPA_HOST_MESSAGE_INTERMNG_H
