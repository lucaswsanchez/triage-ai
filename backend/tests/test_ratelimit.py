from app.ratelimit import DailyBudget, SlidingWindowRateLimiter


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def test_sliding_window_blocks_after_limit_and_recovers():
    clock = Clock()
    limiter = SlidingWindowRateLimiter(3, 3600, clock=clock)
    assert [limiter.allow("1.1.1.1") for _ in range(4)] == [True, True, True, False]
    assert limiter.remaining("1.1.1.1") == 0
    clock.now += 3600
    assert limiter.allow("1.1.1.1")


def test_sliding_window_is_per_key():
    limiter = SlidingWindowRateLimiter(1, 60)
    assert limiter.allow("a")
    assert not limiter.allow("a")
    assert limiter.allow("b")


def test_daily_budget_resets_on_new_day():
    day = {"value": "2026-11-19"}
    budget = DailyBudget(2, today=lambda: day["value"])
    assert [budget.allow() for _ in range(3)] == [True, True, False]
    day["value"] = "2026-11-20"
    assert budget.allow()
