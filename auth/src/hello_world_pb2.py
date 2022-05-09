# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hello_world.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11hello_world.proto\"\"\n\x0fGreetingRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"%\n\x10GreetingResponse\x12\x11\n\tgreetings\x18\x01 \x01(\t\"(\n\x10\x41uthorizeRequest\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\"8\n\x11\x41uthorizeResponse\x12\r\n\x05roles\x18\x01 \x03(\t\x12\x14\n\x0cis_superuser\x18\x02 \x01(\x08\x32h\n\x04\x41uth\x12,\n\x05Greet\x12\x10.GreetingRequest\x1a\x11.GreetingResponse\x12\x32\n\tAuthorize\x12\x11.AuthorizeRequest\x1a\x12.AuthorizeResponseb\x06proto3')



_GREETINGREQUEST = DESCRIPTOR.message_types_by_name['GreetingRequest']
_GREETINGRESPONSE = DESCRIPTOR.message_types_by_name['GreetingResponse']
_AUTHORIZEREQUEST = DESCRIPTOR.message_types_by_name['AuthorizeRequest']
_AUTHORIZERESPONSE = DESCRIPTOR.message_types_by_name['AuthorizeResponse']
GreetingRequest = _reflection.GeneratedProtocolMessageType('GreetingRequest', (_message.Message,), {
  'DESCRIPTOR' : _GREETINGREQUEST,
  '__module__' : 'hello_world_pb2'
  # @@protoc_insertion_point(class_scope:GreetingRequest)
  })
_sym_db.RegisterMessage(GreetingRequest)

GreetingResponse = _reflection.GeneratedProtocolMessageType('GreetingResponse', (_message.Message,), {
  'DESCRIPTOR' : _GREETINGRESPONSE,
  '__module__' : 'hello_world_pb2'
  # @@protoc_insertion_point(class_scope:GreetingResponse)
  })
_sym_db.RegisterMessage(GreetingResponse)

AuthorizeRequest = _reflection.GeneratedProtocolMessageType('AuthorizeRequest', (_message.Message,), {
  'DESCRIPTOR' : _AUTHORIZEREQUEST,
  '__module__' : 'hello_world_pb2'
  # @@protoc_insertion_point(class_scope:AuthorizeRequest)
  })
_sym_db.RegisterMessage(AuthorizeRequest)

AuthorizeResponse = _reflection.GeneratedProtocolMessageType('AuthorizeResponse', (_message.Message,), {
  'DESCRIPTOR' : _AUTHORIZERESPONSE,
  '__module__' : 'hello_world_pb2'
  # @@protoc_insertion_point(class_scope:AuthorizeResponse)
  })
_sym_db.RegisterMessage(AuthorizeResponse)

_AUTH = DESCRIPTOR.services_by_name['Auth']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GREETINGREQUEST._serialized_start=21
  _GREETINGREQUEST._serialized_end=55
  _GREETINGRESPONSE._serialized_start=57
  _GREETINGRESPONSE._serialized_end=94
  _AUTHORIZEREQUEST._serialized_start=96
  _AUTHORIZEREQUEST._serialized_end=136
  _AUTHORIZERESPONSE._serialized_start=138
  _AUTHORIZERESPONSE._serialized_end=194
  _AUTH._serialized_start=196
  _AUTH._serialized_end=300
# @@protoc_insertion_point(module_scope)
