# -*- coding: utf-8 -*-


# noinspection PyUnresolvedReferences
from datetime import datetime, timedelta
import time
import re
import hashlib
from pyorcnews.config.config import IMAGE_URL
import sys
reload(sys)
from pyorcnews.config.config import HOURS
sys.setdefaultencoding('utf8')


def compare_time(datetime_str, date_format="%Y-%m-%d %H:%M:%S", hours=HOURS):
    try:
        date_time = time.strptime(datetime_str[0].decode('UTF-8'), date_format)
    except IndexError:
        return None
    except ValueError:
        return None
    return datetime(*date_time[:5]) if datetime(*date_time[:5]) > \
           datetime.now() - timedelta(hours=hours) else None


def translate_content(elements):
    content = "".join(elements)
    match = re.findall('src="(http://\S*(.jpg|.png|.gif){1})', content)
    images = []
    for match in match:
        images.append(match[0])
        content = content.replace(match[0], IMAGE_URL+hashlib.sha1
        (match[0]).hexdigest() + ".jpg")
    return images, content
