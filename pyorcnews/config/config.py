# -*- coding: utf-8 -*-


def enum(**enums):
    return type('Enum', (object,), enums)


CATEGORY = enum(TECHNOLOGY=1)
IMAGE = 'http://localhost/'
