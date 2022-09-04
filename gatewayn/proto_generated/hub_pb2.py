# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hub.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import tag_pb2 as tag__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\thub.proto\x12\x07gateway\x1a\ttag.proto\"3\n\nHubCommand\x12%\n\x03\x63md\x18\x01 \x01(\x0e\x32\x18.gateway.HubCommandValue\"\x1e\n\x0bHubResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\" \n\rGetTagRequest\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\",\n\x0eGetTagResponse\x12\x1a\n\x04tags\x18\x01 \x03(\x0b\x32\x0c.gateway.Tag*C\n\x0fHubCommandValue\x12\x10\n\x0cStartBLEScan\x10\x00\x12\x1e\n\x1aStartAdvertisementListener\x10\x01\x32\x8e\x01\n\x03Hub\x12I\n\x1aStartAdvertisementScanning\x12\x13.gateway.HubCommand\x1a\x14.gateway.HubResponse\"\x00\x12<\n\x07GetTags\x12\x16.gateway.GetTagRequest\x1a\x17.gateway.GetTagResponse\"\x00\x42<Z:github.com/bchwtz-fhswf/gateway/client/generated;generatedb\x06proto3')

_HUBCOMMANDVALUE = DESCRIPTOR.enum_types_by_name['HubCommandValue']
HubCommandValue = enum_type_wrapper.EnumTypeWrapper(_HUBCOMMANDVALUE)
StartBLEScan = 0
StartAdvertisementListener = 1


_HUBCOMMAND = DESCRIPTOR.message_types_by_name['HubCommand']
_HUBRESPONSE = DESCRIPTOR.message_types_by_name['HubResponse']
_GETTAGREQUEST = DESCRIPTOR.message_types_by_name['GetTagRequest']
_GETTAGRESPONSE = DESCRIPTOR.message_types_by_name['GetTagResponse']
HubCommand = _reflection.GeneratedProtocolMessageType('HubCommand', (_message.Message,), {
  'DESCRIPTOR' : _HUBCOMMAND,
  '__module__' : 'hub_pb2'
  # @@protoc_insertion_point(class_scope:gateway.HubCommand)
  })
_sym_db.RegisterMessage(HubCommand)

HubResponse = _reflection.GeneratedProtocolMessageType('HubResponse', (_message.Message,), {
  'DESCRIPTOR' : _HUBRESPONSE,
  '__module__' : 'hub_pb2'
  # @@protoc_insertion_point(class_scope:gateway.HubResponse)
  })
_sym_db.RegisterMessage(HubResponse)

GetTagRequest = _reflection.GeneratedProtocolMessageType('GetTagRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETTAGREQUEST,
  '__module__' : 'hub_pb2'
  # @@protoc_insertion_point(class_scope:gateway.GetTagRequest)
  })
_sym_db.RegisterMessage(GetTagRequest)

GetTagResponse = _reflection.GeneratedProtocolMessageType('GetTagResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETTAGRESPONSE,
  '__module__' : 'hub_pb2'
  # @@protoc_insertion_point(class_scope:gateway.GetTagResponse)
  })
_sym_db.RegisterMessage(GetTagResponse)

_HUB = DESCRIPTOR.services_by_name['Hub']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z:github.com/bchwtz-fhswf/gateway/client/generated;generated'
  _HUBCOMMANDVALUE._serialized_start=198
  _HUBCOMMANDVALUE._serialized_end=265
  _HUBCOMMAND._serialized_start=33
  _HUBCOMMAND._serialized_end=84
  _HUBRESPONSE._serialized_start=86
  _HUBRESPONSE._serialized_end=116
  _GETTAGREQUEST._serialized_start=118
  _GETTAGREQUEST._serialized_end=150
  _GETTAGRESPONSE._serialized_start=152
  _GETTAGRESPONSE._serialized_end=196
  _HUB._serialized_start=268
  _HUB._serialized_end=410
# @@protoc_insertion_point(module_scope)