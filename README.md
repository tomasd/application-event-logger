application-event-logger
========================

Logs application events into database. Also provides API for accessing these events.

Uses SQLAlchemy as DB backend and blinker for signaling.

Usage
-----
At first configure event logger. You need to create custom mapped class
inherited from `EventObject` and connect it with the signal name:

    >> import sqlalchemy as as, sqlalchemy.orm as orm
    >> from eventlogger import EventLogger
    >> eventlogger = EventLogger(lambda: session)
    >> class UserEvent(eventlogger.EventObject, Base):
            # id, event and created columns are already included in EventObject
            company_id = sa.Column(sa.Integer, sa.ForeignKey('company.id'))
            company = orm.relationship('company')

            customer_id = sa.Column(sa.Integer, sa.ForeignKey('customer.id'))
            customer = orm.relationship('Customer')

            def __repr__(self):
                return '<UserEvent %r, %r, %r, %r >' % (
                    self.created, self.event, self.company, self.user)

    >> user_event = eventlogger.connect('user', UserEvent)

then emit events, through the `eventlogger`

    >> eventlogger.send_signal('user', 'login', company=user.company, user=user)

or directly through the blinker

    >> user_event.send('login', company=user.company, user=user)

finally get and display events in the report

    >> from datetime import date
    >> events = eventlogger.get_events(['user', 'campaign'], start=date(2010, 1, 1))

    >> from pprint import pprint
    >> pprint(events)
    [
      <UserEvent datetime.datetime(2012, 10, 12, 16, 35, 48, 628576), 'login', <Company 1>, <User 1> >,
      <UserEvent datetime.datetime(2012, 10, 12, 16, 35, 49, 628576), 'login', <Company 1>, <User 1> >
    ]
