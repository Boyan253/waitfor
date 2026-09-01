# waitfor

> Wait until a TCP port, HTTP URL or file is ready, then exit - the missing sleep in CI scripts.

## Why

`sleep 10 && run-tests` is a coin flip: too short and the build is flaky, too
long and every CI run pays for it. `waitfor` polls until the thing is actually
up, then returns immediately.

## Usage

```
python waitfor.py tcp://localhost:5432 --timeout 60
python waitfor.py https://localhost:8080/health --expect 200
python waitfor.py file:///tmp/migrations.done
python waitfor.py db:5432 redis:6379 api:8000      # several at once
```

Exit code 0 when everything came up, 1 on timeout.

## Target forms

| form | checks |
|------|--------|
| `tcp://host:port` or `host:port` | a TCP connection can be opened |
| `http://…` / `https://…` | a request returns < 400, or `--expect CODE` |
| `file:///path` or a bare path | the file exists and is non-empty |
