from extensions import db

from ..fixtures._arb_translation import translation
from ..models import *


def upload():
    langs = ['EN', 'GE', 'UA', 'RU']
    id = 0
    for i in langs:
        for item in translation:
            id += 1
            item['id'] = id
            item['language_code'] = i
            tr = Translation(**item)
            db.session.add(tr)
    db.session.commit()
        