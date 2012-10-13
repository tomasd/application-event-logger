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
        self.Session = orm.sessionmaker(bind=self.connection)
        self.session = self.Session()
        Model.bind = self.connection
        Model.metadata.create_all(bind=self.connection)
        self.eventlogger = eventlogger.EventLogger(lambda : self.session)


    def test_connect(self):
        self.eventlogger.connect('user', MyEvent)

    def test_emit(self):
        self.eventlogger.connect('user', MyEvent)

        self.eventlogger.send_signal('user', 'login')

        events = self.eventlogger.get_events('user')

        self.assertEquals(1, len(events))

        [event] = events
        self.assertEquals('login', event.event)

    def test_emit_through_signal(self):
        signal = self.eventlogger.connect('user', MyEvent)

        signal.send('login')

        events = self.eventlogger.get_events('user')

        self.assertEquals(1, len(events))

        [event] = events
        self.assertEquals('login', event.event)

    def test_emit_param(self):
        self.eventlogger.connect('user', MyEvent)



        self.eventlogger.send_signal('user', 'login', param='xxx')

        events = self.eventlogger.get_events('user')

        self.assertEquals(1, len(events))

        [event] = events
        self.assertEquals('xxx', event.param)

