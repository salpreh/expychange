import unittest

from expychange.emitter import Emitter # pylint: disable=import-error
from expychange.exchanges import SimpleExchange # pylint: disable=import-error
from expychange.listener import Listener # pylint: disable=import-error
from expychange.processor import CallbackEventProcessor # pylint: disable=import-error


class TestEventsProcessing(unittest.TestCase):
    TEST_CHANNEL = "channel1"

    def test_simple_event_processing(self):
        processed_data = []
        callback = lambda e: processed_data.append(e)

        exchange = SimpleExchange()
        emitter = Emitter(exchange, self.TEST_CHANNEL)
        Listener(exchange, self.TEST_CHANNEL, CallbackEventProcessor(callback))

        self.assertEqual(0, len(processed_data))

        str_ev = "Some event"
        emitter.emit(str_ev)

        self.assertEqual(1, len(processed_data))
        self.assertEqual(str_ev, processed_data[0])