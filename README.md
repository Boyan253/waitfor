# waitfor

> Wait until a TCP port, HTTP URL or file is ready, then exit - the missing sleep in CI scripts.

## Why

`sleep 10 && run-tests` is a coin flip: too short and the build is flaky, too
long and every CI run pays for it. `waitfor` polls until the thing is actually
up, then returns immediately.
