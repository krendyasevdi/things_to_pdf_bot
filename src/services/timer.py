__all__ = ['CountdownTimer']

import asyncio


class CountdownTimer:
    def __init__(self, duration, callback):
        self.duration = duration
        self.callback = callback
        self.start_time = None
        self._task = None

    async def start(self):
        self.start_time = asyncio.get_event_loop().time()
        self._task = asyncio.create_task(self._run())

    async def _run(self):
        try:
            await asyncio.sleep(self.duration)
            self.callback()
        except asyncio.CancelledError:
            self.start_time = None

    def time_left(self):
        if self.start_time is None:
            return 0
        elapsed = asyncio.get_event_loop().time() - self.start_time
        return max(0, self.duration - elapsed)

    def cancel(self):
        if self._task is not None:
            self._task.cancel()
            self.start_time = None
