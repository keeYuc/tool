# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file-center/image.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='file-center/image.proto',
  package='file_center',
  syntax='proto3',
  serialized_options=b'Z\035app/protocol/grpc/file-center',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17\x66ile-center/image.proto\x12\x0b\x66ile_center\"Q\n\x0eUploadImageReq\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x13\n\x0bimg_content\x18\x02 \x01(\x0c\x12\x1a\n\x12\x63lose_img_compress\x18\x03 \x01(\t\"*\n\x0fUploadImageResp\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\tB\x1fZ\x1d\x61pp/protocol/grpc/file-centerb\x06proto3'
)




_UPLOADIMAGEREQ = _descriptor.Descriptor(
  name='UploadImageReq',
  full_name='file_center.UploadImageReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='file_center.UploadImageReq.app_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='img_content', full_name='file_center.UploadImageReq.img_content', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='close_img_compress', full_name='file_center.UploadImageReq.close_img_compress', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=40,
  serialized_end=121,
)


_UPLOADIMAGERESP = _descriptor.Descriptor(
  name='UploadImageResp',
  full_name='file_center.UploadImageResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='file_center.UploadImageResp.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='file_center.UploadImageResp.url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=123,
  serialized_end=165,
)

DESCRIPTOR.message_types_by_name['UploadImageReq'] = _UPLOADIMAGEREQ
DESCRIPTOR.message_types_by_name['UploadImageResp'] = _UPLOADIMAGERESP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UploadImageReq = _reflection.GeneratedProtocolMessageType('UploadImageReq', (_message.Message,), {
  'DESCRIPTOR' : _UPLOADIMAGEREQ,
  '__module__' : 'file_center.image_pb2'
  # @@protoc_insertion_point(class_scope:file_center.UploadImageReq)
  })
_sym_db.RegisterMessage(UploadImageReq)

UploadImageResp = _reflection.GeneratedProtocolMessageType('UploadImageResp', (_message.Message,), {
  'DESCRIPTOR' : _UPLOADIMAGERESP,
  '__module__' : 'file_center.image_pb2'
  # @@protoc_insertion_point(class_scope:file_center.UploadImageResp)
  })
_sym_db.RegisterMessage(UploadImageResp)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)