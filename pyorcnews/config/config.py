# -*- coding: utf-8 -*-

def enum(**enums):
    return type('Enum', (object,), enums)


CATEGORY = enum(TECHNOLOGY=1)
IMAGE_URL = 'http://wwww.pyorc.com/images/news/full/'
HOURS = 6
