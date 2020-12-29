# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: comix.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='comix.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x08comix.proto\"*\n\x0eIssueResponse2\x12\x18\n\x06issues\x18\x02 \x01(\x0b\x32\x08.Issues2\"(\n\rIssueResponse\x12\x17\n\x06issues\x18\x02 \x01(\x0b\x32\x07.Issues\"\"\n\x07Issues2\x12\x17\n\x06issues\x18\x03 \x03(\x0b\x32\x07.Issue2\" \n\x06Issues\x12\x16\n\x06issues\x18\x03 \x03(\x0b\x32\x06.Issue\"\x14\n\x06Issue2\x12\n\n\x02id\x18\x01 \x01(\t\"T\n\x05Issue\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tseries_id\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\x12\r\n\x05issue\x18\x04 \x01(\t\x12\x0e\n\x06volume\x18\x05 \x01(\t\"S\n\x11OrderRequestProto\x12#\n\x04user\x18\x01 \x02(\x0b\x32\x15.UserCredentialsProto\x12\x19\n\x05items\x18\x02 \x03(\x0b\x32\n.ItemProto\"P\n\x14UserCredentialsProto\x12$\n\x05merch\x18\x01 \x02(\x0b\x32\x15.MerchantAccountProto\x12\x12\n\nauth_token\x18\x03 \x01(\t\"*\n\x14MerchantAccountProto\x12\x12\n\nidentifier\x18\x02 \x02(\t\"\x1c\n\tItemProto\x12\x0f\n\x07item_id\x18\x01 \x02(\r\"=\n\rComicResponse\x12\x15\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x06.Error\x12\x15\n\x05\x63omic\x18\x02 \x01(\x0b\x32\x06.Comic\"\x19\n\x05\x45rror\x12\x10\n\x08\x65rrormsg\x18\x02 \x01(\t\"^\n\x05\x43omic\x12\x10\n\x08\x63omic_id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x19\n\x05issue\x18\x03 \x01(\x0b\x32\n.IssueInfo\x12\x17\n\x04\x62ook\x18\x04 \x01(\x0b\x32\t.BookInfo\"\x9a\x01\n\tIssueInfo\x12\r\n\x05title\x18\x01 \x01(\t\x12\x1d\n\tpublisher\x18\x02 \x01(\x0b\x32\n.Publisher\x12\x17\n\x06series\x18\x03 \x01(\x0b\x32\x07.Series\x12!\n\x12print_release_date\x18\x05 \x01(\x0b\x32\x05.Date\x12#\n\x14\x64igital_release_date\x18\x06 \x01(\x0b\x32\x05.Date\"!\n\tPublisher\x12\x14\n\x0cpublisher_id\x18\x01 \x01(\t\"\x17\n\x06Series\x12\r\n\x05issue\x18\x08 \x01(\r\"0\n\x04\x44\x61te\x12\x0c\n\x04year\x18\x01 \x01(\r\x12\r\n\x05month\x18\x02 \x01(\r\x12\x0b\n\x03\x64\x61y\x18\x03 \x01(\r\" \n\x08\x42ookInfo\x12\x14\n\x05pages\x18\x05 \x03(\x0b\x32\x05.Page\"#\n\x04Page\x12\x1b\n\x08pageinfo\x18\x03 \x01(\x0b\x32\t.PageInfo\"\"\n\x08PageInfo\x12\x16\n\x06images\x18\x01 \x03(\x0b\x32\x06.Image\"\x8a\x01\n\x05Image\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x19\n\x04type\x18\x06 \x01(\x0e\x32\x0b.Image.Type\x12\x17\n\x06\x64igest\x18\x07 \x01(\x0b\x32\x07.Digest\x12\x18\n\x07\x65\x64igest\x18\x08 \x01(\x0b\x32\x07.Digest\"&\n\x04Type\x12\t\n\x05OTHER\x10\x00\x12\t\n\x05THUMB\x10\x01\x12\x08\n\x04\x46ULL\x10\x02\"\x16\n\x06\x44igest\x12\x0c\n\x04\x64\x61ta\x18\x07 \x01(\x0c'
)



_IMAGE_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='Image.Type',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OTHER', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='THUMB', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FULL', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1178,
  serialized_end=1216,
)
_sym_db.RegisterEnumDescriptor(_IMAGE_TYPE)


_ISSUERESPONSE2 = _descriptor.Descriptor(
  name='IssueResponse2',
  full_name='IssueResponse2',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='issues', full_name='IssueResponse2.issues', index=0,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=12,
  serialized_end=54,
)


_ISSUERESPONSE = _descriptor.Descriptor(
  name='IssueResponse',
  full_name='IssueResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='issues', full_name='IssueResponse.issues', index=0,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=56,
  serialized_end=96,
)


_ISSUES2 = _descriptor.Descriptor(
  name='Issues2',
  full_name='Issues2',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='issues', full_name='Issues2.issues', index=0,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=98,
  serialized_end=132,
)


_ISSUES = _descriptor.Descriptor(
  name='Issues',
  full_name='Issues',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='issues', full_name='Issues.issues', index=0,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=134,
  serialized_end=166,
)


_ISSUE2 = _descriptor.Descriptor(
  name='Issue2',
  full_name='Issue2',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Issue2.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=168,
  serialized_end=188,
)


_ISSUE = _descriptor.Descriptor(
  name='Issue',
  full_name='Issue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Issue.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='series_id', full_name='Issue.series_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='title', full_name='Issue.title', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='issue', full_name='Issue.issue', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='volume', full_name='Issue.volume', index=4,
      number=5, type=9, cpp_type=9, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=190,
  serialized_end=274,
)


_ORDERREQUESTPROTO = _descriptor.Descriptor(
  name='OrderRequestProto',
  full_name='OrderRequestProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user', full_name='OrderRequestProto.user', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='items', full_name='OrderRequestProto.items', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=276,
  serialized_end=359,
)


_USERCREDENTIALSPROTO = _descriptor.Descriptor(
  name='UserCredentialsProto',
  full_name='UserCredentialsProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='merch', full_name='UserCredentialsProto.merch', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='auth_token', full_name='UserCredentialsProto.auth_token', index=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=361,
  serialized_end=441,
)


_MERCHANTACCOUNTPROTO = _descriptor.Descriptor(
  name='MerchantAccountProto',
  full_name='MerchantAccountProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='identifier', full_name='MerchantAccountProto.identifier', index=0,
      number=2, type=9, cpp_type=9, label=2,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=443,
  serialized_end=485,
)


_ITEMPROTO = _descriptor.Descriptor(
  name='ItemProto',
  full_name='ItemProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='item_id', full_name='ItemProto.item_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=487,
  serialized_end=515,
)


_COMICRESPONSE = _descriptor.Descriptor(
  name='ComicResponse',
  full_name='ComicResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='ComicResponse.error', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='comic', full_name='ComicResponse.comic', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=517,
  serialized_end=578,
)


_ERROR = _descriptor.Descriptor(
  name='Error',
  full_name='Error',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='errormsg', full_name='Error.errormsg', index=0,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=580,
  serialized_end=605,
)


_COMIC = _descriptor.Descriptor(
  name='Comic',
  full_name='Comic',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='comic_id', full_name='Comic.comic_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='Comic.version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='issue', full_name='Comic.issue', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='book', full_name='Comic.book', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=607,
  serialized_end=701,
)


_ISSUEINFO = _descriptor.Descriptor(
  name='IssueInfo',
  full_name='IssueInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='IssueInfo.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='publisher', full_name='IssueInfo.publisher', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='series', full_name='IssueInfo.series', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='print_release_date', full_name='IssueInfo.print_release_date', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='digital_release_date', full_name='IssueInfo.digital_release_date', index=4,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=704,
  serialized_end=858,
)


_PUBLISHER = _descriptor.Descriptor(
  name='Publisher',
  full_name='Publisher',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='publisher_id', full_name='Publisher.publisher_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=860,
  serialized_end=893,
)


_SERIES = _descriptor.Descriptor(
  name='Series',
  full_name='Series',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='issue', full_name='Series.issue', index=0,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=895,
  serialized_end=918,
)


_DATE = _descriptor.Descriptor(
  name='Date',
  full_name='Date',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='year', full_name='Date.year', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='month', full_name='Date.month', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='day', full_name='Date.day', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=920,
  serialized_end=968,
)


_BOOKINFO = _descriptor.Descriptor(
  name='BookInfo',
  full_name='BookInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pages', full_name='BookInfo.pages', index=0,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=970,
  serialized_end=1002,
)


_PAGE = _descriptor.Descriptor(
  name='Page',
  full_name='Page',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pageinfo', full_name='Page.pageinfo', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1004,
  serialized_end=1039,
)


_PAGEINFO = _descriptor.Descriptor(
  name='PageInfo',
  full_name='PageInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='images', full_name='PageInfo.images', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1041,
  serialized_end=1075,
)


_IMAGE = _descriptor.Descriptor(
  name='Image',
  full_name='Image',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='uri', full_name='Image.uri', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='Image.type', index=1,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='digest', full_name='Image.digest', index=2,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='edigest', full_name='Image.edigest', index=3,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _IMAGE_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1078,
  serialized_end=1216,
)


_DIGEST = _descriptor.Descriptor(
  name='Digest',
  full_name='Digest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='Digest.data', index=0,
      number=7, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1218,
  serialized_end=1240,
)

_ISSUERESPONSE2.fields_by_name['issues'].message_type = _ISSUES2
_ISSUERESPONSE.fields_by_name['issues'].message_type = _ISSUES
_ISSUES2.fields_by_name['issues'].message_type = _ISSUE2
_ISSUES.fields_by_name['issues'].message_type = _ISSUE
_ORDERREQUESTPROTO.fields_by_name['user'].message_type = _USERCREDENTIALSPROTO
_ORDERREQUESTPROTO.fields_by_name['items'].message_type = _ITEMPROTO
_USERCREDENTIALSPROTO.fields_by_name['merch'].message_type = _MERCHANTACCOUNTPROTO
_COMICRESPONSE.fields_by_name['error'].message_type = _ERROR
_COMICRESPONSE.fields_by_name['comic'].message_type = _COMIC
_COMIC.fields_by_name['issue'].message_type = _ISSUEINFO
_COMIC.fields_by_name['book'].message_type = _BOOKINFO
_ISSUEINFO.fields_by_name['publisher'].message_type = _PUBLISHER
_ISSUEINFO.fields_by_name['series'].message_type = _SERIES
_ISSUEINFO.fields_by_name['print_release_date'].message_type = _DATE
_ISSUEINFO.fields_by_name['digital_release_date'].message_type = _DATE
_BOOKINFO.fields_by_name['pages'].message_type = _PAGE
_PAGE.fields_by_name['pageinfo'].message_type = _PAGEINFO
_PAGEINFO.fields_by_name['images'].message_type = _IMAGE
_IMAGE.fields_by_name['type'].enum_type = _IMAGE_TYPE
_IMAGE.fields_by_name['digest'].message_type = _DIGEST
_IMAGE.fields_by_name['edigest'].message_type = _DIGEST
_IMAGE_TYPE.containing_type = _IMAGE
DESCRIPTOR.message_types_by_name['IssueResponse2'] = _ISSUERESPONSE2
DESCRIPTOR.message_types_by_name['IssueResponse'] = _ISSUERESPONSE
DESCRIPTOR.message_types_by_name['Issues2'] = _ISSUES2
DESCRIPTOR.message_types_by_name['Issues'] = _ISSUES
DESCRIPTOR.message_types_by_name['Issue2'] = _ISSUE2
DESCRIPTOR.message_types_by_name['Issue'] = _ISSUE
DESCRIPTOR.message_types_by_name['OrderRequestProto'] = _ORDERREQUESTPROTO
DESCRIPTOR.message_types_by_name['UserCredentialsProto'] = _USERCREDENTIALSPROTO
DESCRIPTOR.message_types_by_name['MerchantAccountProto'] = _MERCHANTACCOUNTPROTO
DESCRIPTOR.message_types_by_name['ItemProto'] = _ITEMPROTO
DESCRIPTOR.message_types_by_name['ComicResponse'] = _COMICRESPONSE
DESCRIPTOR.message_types_by_name['Error'] = _ERROR
DESCRIPTOR.message_types_by_name['Comic'] = _COMIC
DESCRIPTOR.message_types_by_name['IssueInfo'] = _ISSUEINFO
DESCRIPTOR.message_types_by_name['Publisher'] = _PUBLISHER
DESCRIPTOR.message_types_by_name['Series'] = _SERIES
DESCRIPTOR.message_types_by_name['Date'] = _DATE
DESCRIPTOR.message_types_by_name['BookInfo'] = _BOOKINFO
DESCRIPTOR.message_types_by_name['Page'] = _PAGE
DESCRIPTOR.message_types_by_name['PageInfo'] = _PAGEINFO
DESCRIPTOR.message_types_by_name['Image'] = _IMAGE
DESCRIPTOR.message_types_by_name['Digest'] = _DIGEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

IssueResponse2 = _reflection.GeneratedProtocolMessageType('IssueResponse2', (_message.Message,), {
  'DESCRIPTOR' : _ISSUERESPONSE2,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:IssueResponse2)
  })
_sym_db.RegisterMessage(IssueResponse2)

IssueResponse = _reflection.GeneratedProtocolMessageType('IssueResponse', (_message.Message,), {
  'DESCRIPTOR' : _ISSUERESPONSE,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:IssueResponse)
  })
_sym_db.RegisterMessage(IssueResponse)

Issues2 = _reflection.GeneratedProtocolMessageType('Issues2', (_message.Message,), {
  'DESCRIPTOR' : _ISSUES2,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:Issues2)
  })
_sym_db.RegisterMessage(Issues2)

Issues = _reflection.GeneratedProtocolMessageType('Issues', (_message.Message,), {
  'DESCRIPTOR' : _ISSUES,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:Issues)
  })
_sym_db.RegisterMessage(Issues)

Issue2 = _reflection.GeneratedProtocolMessageType('Issue2', (_message.Message,), {
  'DESCRIPTOR' : _ISSUE2,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:Issue2)
  })
_sym_db.RegisterMessage(Issue2)

Issue = _reflection.GeneratedProtocolMessageType('Issue', (_message.Message,), {
  'DESCRIPTOR' : _ISSUE,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:Issue)
  })
_sym_db.RegisterMessage(Issue)

OrderRequestProto = _reflection.GeneratedProtocolMessageType('OrderRequestProto', (_message.Message,), {
  'DESCRIPTOR' : _ORDERREQUESTPROTO,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:OrderRequestProto)
  })
_sym_db.RegisterMessage(OrderRequestProto)

UserCredentialsProto = _reflection.GeneratedProtocolMessageType('UserCredentialsProto', (_message.Message,), {
  'DESCRIPTOR' : _USERCREDENTIALSPROTO,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:UserCredentialsProto)
  })
_sym_db.RegisterMessage(UserCredentialsProto)

MerchantAccountProto = _reflection.GeneratedProtocolMessageType('MerchantAccountProto', (_message.Message,), {
  'DESCRIPTOR' : _MERCHANTACCOUNTPROTO,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:MerchantAccountProto)
  })
_sym_db.RegisterMessage(MerchantAccountProto)

ItemProto = _reflection.GeneratedProtocolMessageType('ItemProto', (_message.Message,), {
  'DESCRIPTOR' : _ITEMPROTO,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:ItemProto)
  })
_sym_db.RegisterMessage(ItemProto)

ComicResponse = _reflection.GeneratedProtocolMessageType('ComicResponse', (_message.Message,), {
  'DESCRIPTOR' : _COMICRESPONSE,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:ComicResponse)
  })
_sym_db.RegisterMessage(ComicResponse)

Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
  'DESCRIPTOR' : _ERROR,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:Error)
  })
_sym_db.RegisterMessage(Error)

Comic = _reflection.GeneratedProtocolMessageType('Comic', (_message.Message,), {
  'DESCRIPTOR' : _COMIC,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:Comic)
  })
_sym_db.RegisterMessage(Comic)

IssueInfo = _reflection.GeneratedProtocolMessageType('IssueInfo', (_message.Message,), {
  'DESCRIPTOR' : _ISSUEINFO,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:IssueInfo)
  })
_sym_db.RegisterMessage(IssueInfo)

Publisher = _reflection.GeneratedProtocolMessageType('Publisher', (_message.Message,), {
  'DESCRIPTOR' : _PUBLISHER,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:Publisher)
  })
_sym_db.RegisterMessage(Publisher)

Series = _reflection.GeneratedProtocolMessageType('Series', (_message.Message,), {
  'DESCRIPTOR' : _SERIES,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:Series)
  })
_sym_db.RegisterMessage(Series)

Date = _reflection.GeneratedProtocolMessageType('Date', (_message.Message,), {
  'DESCRIPTOR' : _DATE,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:Date)
  })
_sym_db.RegisterMessage(Date)

BookInfo = _reflection.GeneratedProtocolMessageType('BookInfo', (_message.Message,), {
  'DESCRIPTOR' : _BOOKINFO,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:BookInfo)
  })
_sym_db.RegisterMessage(BookInfo)

Page = _reflection.GeneratedProtocolMessageType('Page', (_message.Message,), {
  'DESCRIPTOR' : _PAGE,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:Page)
  })
_sym_db.RegisterMessage(Page)

PageInfo = _reflection.GeneratedProtocolMessageType('PageInfo', (_message.Message,), {
  'DESCRIPTOR' : _PAGEINFO,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:PageInfo)
  })
_sym_db.RegisterMessage(PageInfo)

Image = _reflection.GeneratedProtocolMessageType('Image', (_message.Message,), {
  'DESCRIPTOR' : _IMAGE,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:Image)
  })
_sym_db.RegisterMessage(Image)

Digest = _reflection.GeneratedProtocolMessageType('Digest', (_message.Message,), {
  'DESCRIPTOR' : _DIGEST,
  '__module__' : 'comix_pb2'
  # @@protoc_insertion_point(class_scope:Digest)
  })
_sym_db.RegisterMessage(Digest)


# @@protoc_insertion_point(module_scope)
