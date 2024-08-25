import signal
import asyncio
import logging

logger = logging.getLogger(__name__)


class TerminationHandler:

    @property
    def stop_event(self):
        return self._stop_event

    def __init__(self):
        self._stop_event = asyncio.Event()

    def _handle_stop_event(self, _sig, _frame):
        logger.info(f"Received signal {_sig} at frame {_frame}")
        self.stop_event.set()

    def register_terminate_signal(self):
        signal.signal(signal.SIGINT, self._handle_stop_event)
        signal.signal(signal.SIGTERM, self._handle_stop_event)
