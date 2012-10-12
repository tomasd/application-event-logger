import unittest
import sqlalchemy as sa
import sqlalchemy.orm as orm
import eventlogger
from sqlalchemy.ext.declarative import declarative_base


Model = declarative_base()

class MyEvent(eventlogger.EventObject, Model):
    __tablename__ = 'myevent'

    param = sa.Column(sa.String(255))


class EventLoggerTest(unittest.TestCase):
    def setUp(self):
        self.connection = sa.create_engine('sqlite://')
        Session = orm.sessionmaker(bind=self.connection)
        self.session = Session()
        Model.bind = self.connection
        Model.metadata.create_all(bind=self.connection)



    def test_connect(self):
        eventlogger.connect('user', MyEvent)

    def test_emit(self):
        eventlogger.connect('user', MyEvent)

        eventlogger.open(self.session)

        eventlogger.send_signal('user', 'login')

        events = eventlogger.get_events('user')

        self.assertEquals(1, len(events))

        [event] = events
        self.assertEquals('login', event.event)

    def test_emit_through_signal(self):
        signal = eventlogger.connect('user', MyEvent)

        eventlogger.open(self.session)

        signal.send('login')

        events = eventlogger.get_events('user')

        self.assertEquals(1, len(events))

        [event] = events
        self.assertEquals('login', event.event)

    def test_emit_param(self):
        eventlogger.connect('user', MyEvent)

        eventlogger.open(self.session)

        eventlogger.send_signal('user', 'login', param='xxx')

        events = eventlogger.get_events('user')

        self.assertEquals(1, len(events))

        [event] = events
        self.assertEquals('xxx', event.param)

