# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: seo/seo_service.proto
"""Generated protocol buffer code."""
from protocol.seo import data_pb2 as data__pb2
from protocol import common_pb2 as common__pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name='seo/seo_service.proto',
    package='seo',
    syntax='proto3',
    serialized_options=b'Z\025app/protocol/grpc/seo',
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x15seo/seo_service.proto\x12\x03seo\x1a\x0c\x63ommon.proto\x1a\ndata.proto2\xdc\x03\n\nSeoService\x12*\n\tQueryShop\x12\x11.common.QueryInfo\x1a\n.seo.Shops\x12\x36\n\x13QueryShopByDistance\x12\x13.seo.ByDistanceInfo\x1a\n.seo.Shops\x12\x30\n\x0cQueryComment\x12\x11.common.QueryInfo\x1a\r.seo.Comments\x12(\n\nCreateShop\x12\x0c.seo.ShopReq\x1a\x0c.seo.ShopRsb\x12(\n\nUpdateShop\x12\x0c.seo.ShopReq\x1a\x0c.seo.ShopRsb\x12\x34\n\x0e\x43reateComments\x12\x10.seo.CommentsReq\x1a\x10.seo.CommentsRsb\x12\x34\n\x0eUpdateComments\x12\x10.seo.CommentsReq\x1a\x10.seo.CommentsRsb\x12\x38\n\x0cQueryShopTag\x12\x11.common.QueryInfo\x1a\x15.seo.QueryShopTagResp\x12>\n\rCreateShopTag\x12\x15.seo.CreateShopTagReq\x1a\x16.seo.CreateShopTagRespB\x17Z\x15\x61pp/protocol/grpc/seob\x06proto3',
    dependencies=[common__pb2.DESCRIPTOR, data__pb2.DESCRIPTOR, ])


_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_SEOSERVICE = _descriptor.ServiceDescriptor(
    name='SeoService',
    full_name='seo.SeoService',
    file=DESCRIPTOR,
    index=0,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_start=57,
    serialized_end=533,
    methods=[
        _descriptor.MethodDescriptor(
            name='QueryShop',
            full_name='seo.SeoService.QueryShop',
            index=0,
            containing_service=None,
            input_type=common__pb2._QUERYINFO,
            output_type=data__pb2._SHOPS,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name='QueryShopByDistance',
            full_name='seo.SeoService.QueryShopByDistance',
            index=1,
            containing_service=None,
            input_type=data__pb2._BYDISTANCEINFO,
            output_type=data__pb2._SHOPS,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name='QueryComment',
            full_name='seo.SeoService.QueryComment',
            index=2,
            containing_service=None,
            input_type=common__pb2._QUERYINFO,
            output_type=data__pb2._COMMENTS,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name='CreateShop',
            full_name='seo.SeoService.CreateShop',
            index=3,
            containing_service=None,
            input_type=data__pb2._SHOPREQ,
            output_type=data__pb2._SHOPRSB,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name='UpdateShop',
            full_name='seo.SeoService.UpdateShop',
            index=4,
            containing_service=None,
            input_type=data__pb2._SHOPREQ,
            output_type=data__pb2._SHOPRSB,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name='CreateComments',
            full_name='seo.SeoService.CreateComments',
            index=5,
            containing_service=None,
            input_type=data__pb2._COMMENTSREQ,
            output_type=data__pb2._COMMENTSRSB,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name='UpdateComments',
            full_name='seo.SeoService.UpdateComments',
            index=6,
            containing_service=None,
            input_type=data__pb2._COMMENTSREQ,
            output_type=data__pb2._COMMENTSRSB,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name='QueryShopTag',
            full_name='seo.SeoService.QueryShopTag',
            index=7,
            containing_service=None,
            input_type=common__pb2._QUERYINFO,
            output_type=data__pb2._QUERYSHOPTAGRESP,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name='CreateShopTag',
            full_name='seo.SeoService.CreateShopTag',
            index=8,
            containing_service=None,
            input_type=data__pb2._CREATESHOPTAGREQ,
            output_type=data__pb2._CREATESHOPTAGRESP,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
    ])
_sym_db.RegisterServiceDescriptor(_SEOSERVICE)

DESCRIPTOR.services_by_name['SeoService'] = _SEOSERVICE

# @@protoc_insertion_point(module_scope)
