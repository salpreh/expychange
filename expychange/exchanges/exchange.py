from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from expychange.listener import Listener


class Exchange(metaclass = ABCMeta):

    @abstractmethod
    def register_channel(self, channel_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_listener(self, listener: 'Listener', channel_name: str):
        raise NotImplementedError

    @abstractmethod
    def emit_event(self, channel_name: str, event: Any) -> None:
        raise NotImplementedError