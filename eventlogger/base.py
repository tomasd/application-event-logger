import functools
import blinker


class EventLogger(object):
    _classes = {}
    _signals = {}

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def connect(self, event_class_name, event_class):
        def _log_event(event_class_name, event,
                       **kwargs):
            EventClass = self._get_event_class(event_class_name)

            obj = EventClass(event=event, **kwargs)

            session.add(obj)
            session.flush()

        session = self.session_factory()

        self._save_event_class(event_class_name, event_class)

        blinker_signal = blinker.signal(event_class_name)
        self._save_event_signal(event_class_name, blinker_signal)

        log_function = functools.partial(_log_event,event_class_name)
        blinker_signal.connect(log_function, weak=False)
        return blinker_signal


    def send_signal(self, event_class_name, event, **kwargs):
        signal = self._get_event_signal(event_class_name)
        signal.send(event, **kwargs)


    def get_events(self, event_class_name):
        event_class = self._get_event_class(event_class_name)

        session = self.session_factory()
        return session.query(event_class).all()


    def _get_event_class(self, event_class_name):
        return self._classes[event_class_name]


    def _save_event_class(self, event_class_name, event_class):
        self._remove_signal(event_class_name)

        self._classes[event_class_name] = event_class


    def _get_event_signal(self, event_class_name):
        return self._signals[event_class_name]


    def _save_event_signal(self, event_class_name, signal):
        self._signals[event_class_name] = signal


    def _remove_signal(self, event_class_name):
        self._signals.pop(event_class_name, None)


