# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file-center/file_center_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import image_pb2 as image__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='file-center/file_center_service.proto',
  package='file_center',
  syntax='proto3',
  serialized_options=b'Z\035app/protocol/grpc/file-center',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%file-center/file_center_service.proto\x12\x0b\x66ile_center\x1a\x0bimage.proto2]\n\x11\x46ileCenterService\x12H\n\x0bUploadImage\x12\x1b.file_center.UploadImageReq\x1a\x1c.file_center.UploadImageRespB\x1fZ\x1d\x61pp/protocol/grpc/file-centerb\x06proto3'
  ,
  dependencies=[image__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_FILECENTERSERVICE = _descriptor.ServiceDescriptor(
  name='FileCenterService',
  full_name='file_center.FileCenterService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=67,
  serialized_end=160,
  methods=[
  _descriptor.MethodDescriptor(
    name='UploadImage',
    full_name='file_center.FileCenterService.UploadImage',
    index=0,
    containing_service=None,
    input_type=image__pb2._UPLOADIMAGEREQ,
    output_type=image__pb2._UPLOADIMAGERESP,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_FILECENTERSERVICE)

DESCRIPTOR.services_by_name['FileCenterService'] = _FILECENTERSERVICE

# @@protoc_insertion_point(module_scope)