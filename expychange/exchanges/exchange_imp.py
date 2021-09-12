from typing import Dict, List, Any
from queue import Queue

from expychange.listener import Listener
from expychange.exceptions import NoEventsError
from .exchange import Exchange


class SimpleExchange(Exchange):
    """ Simple exchange. Does not store events, serves them to current active listener. If no listener
    during event emision, event will be lost.
    """
    listeners: Dict[str, List[Listener]]

    def __init__(self):
        self.listeners = {}

    def register_channel(self, channel_name: str) -> None:
        if channel_name not in self.listeners:
            self.listeners[channel_name] = []

    def register_listener(self, listener: Listener, channel_name: str):
        self.register_channel(channel_name)
        self.listeners[channel_name].append(listener)

    def emit_event(self, channel_name: str, event: Any) -> None:
        for listener in self.listeners.get(channel_name, []):
            listener.notify(event)


class BufferedExchange(Exchange):
    """ Buffered exchange. Stores last x events per channel if not listeners available. Buffered events will be served
    to first registered listener in a channel.

    Raises:
        NoEventsError: [description]

    Returns:
        [type]: [description]
    """
    channels: Dict[str, Queue]
    listeners: Dict[str, List[Listener]]
    buffer_size: int

    def __init__(self, buffer_size: int = 30):
        # Configure queues
        self.buffer_size = buffer_size
        self.channels = {}
        self.listeners = {}

    def register_channel(self, channel_name: str) -> None:
        if channel_name not in self.channels:
            self.channels[channel_name] = self._create_queue_buffer()

        if channel_name not in self.listeners:
            self.listeners[channel_name] = []

    def register_listener(self, listener: Listener, channel_name: str):
        self.listeners[channel_name].append(listener)
        self._notify_buffered_events(channel_name, listener)

    def emit_event(self, channel_name: str, event: Any) -> None:
        self.register_channel(channel_name)

        # If no listeners buffer and finish
        listeners = self.listeners.get(channel_name, [])
        if not listeners:
            self._add_channel_event(channel_name, event)
            return

        for listener in listeners:
            listener.notify(event)

    def _notify_buffered_events(self, channel_name: str, listener: Listener) -> None:
        channel = self.channels.get(channel_name, self._create_queue_buffer())
        while not channel.empty():
            listener.notify(channel.get())

    def _add_channel_event(self, channel_name: str, event: Any) -> None:
        if not channel_name in self.channels:
            self.register_channel(channel_name)

        channel_q = self.channels[channel_name]
        if (channel_q.full()): channel_q.get()
        channel_q.put(event)

    def _create_queue_buffer(self):
        return Queue(self.buffer_size)