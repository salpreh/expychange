from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from expychange.exchanges import Exchange
    from expychange.processor import EventProcessor


class Listener():
    exchange: 'Exchange'
    channel_name: str
    processor: 'EventProcessor'
    
    def __init__(self, exchange: 'Exchange', channel_name: str, processor: 'EventProcessor'):
        self.exchange = exchange
        self.channel_name = channel_name
        self.processor = processor

        self._init()

    def notify(self, event: Any):
        self.processor.process(event)

    def _init(self):
        self.exchange.register_listener(self, self.channel_name)