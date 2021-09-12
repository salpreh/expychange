from abc import ABCMeta, abstractmethod
from typing import Any, Callable


class EventProcessor(metaclass = ABCMeta):
    @abstractmethod
    def process(self, event: Any) -> None:
        raise NotImplementedError


class CallbackEventProcessor(EventProcessor):
    callback: Callable[[Any], None]
    
    def __init__(self, callback: Callable[[Any], None]):
        self.callback = callback

    def process(self, event: Any) -> None:
        self.callback(event)