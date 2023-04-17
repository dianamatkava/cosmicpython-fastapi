from extensions import db

from ..fixtures._arb_translation import translation
from ..models import *


def upload():
    for item in translation:
        tr = Translation(**item)
        db.session.add(tr)
    db.session.commit()
        