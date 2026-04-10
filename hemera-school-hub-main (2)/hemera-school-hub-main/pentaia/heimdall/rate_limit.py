from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta


@dataclass(slots=True)
class LimitResult:
    allowed: bool
    remaining: int
    reset_seconds: int


class SlidingWindowRateLimiter:
    def __init__(self, requests: int, window_seconds: int):
        self.requests = requests
        self.window = timedelta(seconds=window_seconds)
        self._bucket: dict[str, deque[datetime]] = defaultdict(deque)

    def check(self, key: str) -> LimitResult:
        now = datetime.now(timezone.utc)
        queue = self._bucket[key]
        cutoff = now - self.window
        while queue and queue[0] <= cutoff:
            queue.popleft()

        if len(queue) >= self.requests:
            reset = int((queue[0] + self.window - now).total_seconds())
            return LimitResult(False, 0, max(reset, 0))

        queue.append(now)
        remaining = self.requests - len(queue)
        return LimitResult(True, remaining, int(self.window.total_seconds()))
