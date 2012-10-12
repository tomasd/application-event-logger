import datetime
import sqlalchemy as sa


class EventObject(object):
    id = sa.Column(sa.Integer, primary_key=True)
    created = sa.Column(sa.String(255), default=datetime.datetime.now)
    event = sa.Column(sa.String(255), nullable=False)
