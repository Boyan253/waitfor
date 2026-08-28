import waitfor


def test_wait_returns_immediately_when_ready():
    elapsed = wait_result = waitfor.wait(lambda: True, timeout=5, sleep=lambda _s: None)
    assert wait_result is not None and elapsed >= 0

def test_wait_times_out():
    clock = iter([0, 0, 1, 2, 99])
    assert waitfor.wait(lambda: False, timeout=1, now=lambda: next(clock),
                        sleep=lambda _s: None) is None


def test_wait_succeeds_after_a_few_polls():
    state = {"n": 0}

    def check():
        state["n"] += 1
        return state["n"] >= 3

    assert waitfor.wait(check, timeout=10, sleep=lambda _s: None) is not None
    assert state["n"] == 3

def test_make_check_recognises_tcp():
    _check, label = waitfor.make_check("tcp://localhost:5432")
    assert label == "TCP localhost:5432"


def test_make_check_recognises_http():
    _check, label = waitfor.make_check("https://example.com/health")
    assert label.startswith("HTTP")

def test_make_check_bare_host_port():
    _check, label = waitfor.make_check("db:5432")
    assert label == "TCP db:5432"


def test_file_ready(tmp_path):
    p = tmp_path / "ready"
    assert waitfor.file_ready(str(p)) is False
    p.write_text("x", encoding="utf-8")
    assert waitfor.file_ready(str(p)) is True
