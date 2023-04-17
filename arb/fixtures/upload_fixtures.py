from extensions import db

from ..fixtures._arb_translation import translation
from ..models import *


def upload():
    lang = ['EN', 'GE', 'UA', 'RU']
    id = 0
    for l in lang:
        
        for item in translation:
            id += 1
            item['language_code'] = l
            item['id'] = id
            tr = Translation(**item)
            db.session.add(tr)
    db.session.commit()
        