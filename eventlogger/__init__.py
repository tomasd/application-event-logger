import functools
from eventlogger.model import EventObject
import blinker


_session = None

_classes = {}
_signals = {}


def connect(event_class_name, event_class):
    _save_event_class(event_class_name, event_class)

    blinker_signal = blinker.signal(event_class_name)
    _save_event_signal(event_class_name, blinker_signal)

    log_function = functools.partial(_log_event, event_class_name)
    blinker_signal.connect(log_function, weak=False)
    return blinker_signal


def open(session):
    global _session
    _session = session
    return None


def _log_event(event_class_name, event, **kwargs):
    EventClass = _get_event_class(event_class_name)

    obj = EventClass(event=event, **kwargs)

    session = _get_session()
    session.add(obj)
    session.flush()


def send_signal(event_class_name, event, **kwargs):
    signal = _get_event_signal(event_class_name)
    signal.send(event, **kwargs)
    return None


def get_events(event_class_name):
    event_class = _get_event_class(event_class_name)

    return _session.query(event_class).all()


def _get_event_class(event_class_name):
    return _classes[event_class_name]


def _save_event_class(event_class_name, event_class):
    _remove_signal(event_class_name)

    _classes[event_class_name] = event_class


def _get_event_signal(event_class_name):
    return _signals[event_class_name]


def _save_event_signal(event_class_name, signal):
    _signals[event_class_name] = signal


def _get_session():
    return _session


def _remove_signal(event_class_name):
    _signals.pop(event_class_name, None)


