from typing import Any

from expychange.exchanges import Exchange


class Emitter():
    exchange: Exchange
    channel_name: str

    def __init__(self, exchange: Exchange, channel_name: str):
        self.exchange = exchange
        self.channel_name = channel_name

    def emit(self, event: Any) -> None:
        self.exchange.emit_event(self.channel_name, event)

    def _init(self):
        if self.exchange is not None:
            self.exchange.register_channel(self.channel_name)
