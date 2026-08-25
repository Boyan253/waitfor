import waitfor


def test_wait_returns_immediately_when_ready():
    elapsed = wait_result = waitfor.wait(lambda: True, timeout=5, sleep=lambda _s: None)
    assert wait_result is not None and elapsed >= 0

def test_wait_times_out():
    clock = iter([0, 0, 1, 2, 99])
    assert waitfor.wait(lambda: False, timeout=1, now=lambda: next(clock),
                        sleep=lambda _s: None) is None
