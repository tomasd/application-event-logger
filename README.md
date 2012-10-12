application-event-logger
========================

Logs application events into database. Also provides API for accessing these events.

Uses SQLAlchemy as DB backend and blinker for signaling.

Usage
-----
At first configure event logger

    >> import eventlogger
    >> eventlogger.open(session)

then emit events

    >> eventlogger.send('user', 'login', company=user.company, user=user)

and finally display get and display events in report

    >> from datetime import date
    >> events = eventlogger.get_events(['user', 'campaign'], start=date(2010, 1, 1))
    
    >> from pprint import pprint
    >> pprint(events)
    [
      (datetime.datetime(2012, 10, 12, 16, 35, 48, 628576), 'user', 'login', 1, 2)
    ]

If you are good programmer, then close the logger:
  
    eventlogger.close()