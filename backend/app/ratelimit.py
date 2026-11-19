"""In-memory cost protection: per-IP sliding window and a global daily budget.

State lives in process memory, which is enough for a single free-tier instance. With several
instances it would move to Redis (see the About page: limitations).
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict, deque
from collections.abc import Callable
from datetime import UTC, datetime


class SlidingWindowRateLimiter:
    def __init__(
        self, max_requests: int, window_seconds: int, clock: Callable[[], float] = time.monotonic
    ) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._clock = clock
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def _prune(self, key: str, now: float) -> deque[float]:
        hits = self._hits[key]
        while hits and now - hits[0] >= self.window_seconds:
            hits.popleft()
        return hits

    def allow(self, key: str) -> bool:
        """Consume one request for `key` if it is under the limit."""
        with self._lock:
            now = self._clock()
            hits = self._prune(key, now)
            if len(hits) >= self.max_requests:
                return False
            hits.append(now)
            return True

    def remaining(self, key: str) -> int:
        with self._lock:
            return max(0, self.max_requests - len(self._prune(key, self._clock())))


class DailyBudget:
    """Global cap of live LLM calls per UTC day, whatever the IP."""

    def __init__(self, limit: int, today: Callable[[], str] | None = None) -> None:
        self.limit = limit
        self._today = today or (lambda: datetime.now(UTC).date().isoformat())
        self._day = self._today()
        self._used = 0
        self._lock = threading.Lock()

    def allow(self) -> bool:
        with self._lock:
            day = self._today()
            if day != self._day:
                self._day, self._used = day, 0
            if self._used >= self.limit:
                return False
            self._used += 1
            return True
