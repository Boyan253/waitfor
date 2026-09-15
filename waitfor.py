#!/usr/bin/env python3
"""Block until a port, URL or file becomes available."""

import argparse
import os
import socket
import sys
import time
import urllib.error
import urllib.request

__version__ = "0.1.0"


def tcp_ready(host, port, timeout=2.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def http_ready(url, timeout=5.0, expect=None):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status < 400 if expect is None else resp.status == expect
    except urllib.error.HTTPError as exc:
        return exc.code == expect if expect is not None else False
    except (urllib.error.URLError, OSError):
        return False


def file_ready(path, min_size=1):
    try:
        return os.path.getsize(path) >= min_size
    except OSError:
        return False


def make_check(target, expect=None):
    """Turn a target string into a zero-argument predicate."""
    if target.startswith(("http://", "https://")):
        return lambda: http_ready(target, expect=expect), "HTTP %s" % target
    if target.startswith("tcp://"):
        host, _, port = target[6:].rpartition(":")
        return lambda: tcp_ready(host or "localhost", int(port)), "TCP %s:%s" % (host, port)
    if target.startswith("file://"):
        path = target[7:]
        return lambda: file_ready(path), "file %s" % path
    if ":" in target and target.rsplit(":", 1)[1].isdigit():
        host, _, port = target.rpartition(":")
        return lambda: tcp_ready(host or "localhost", int(port)), "TCP %s:%s" % (host, port)
    return lambda: file_ready(target), "file %s" % target


def wait(check, timeout=60.0, interval=0.5, now=time.monotonic, sleep=time.sleep):
    """Poll check() until it is true or the timeout expires. Returns elapsed or None."""
    deadline = now() + timeout
    started = now()
    while True:
        if check():
            return now() - started
        if now() >= deadline:
            return None
        sleep(interval)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + __version__)
    ap.add_argument("targets", nargs="+",
                    help="tcp://host:port, http(s)://url, file://path, or host:port")
    ap.add_argument("-t", "--timeout", type=float, default=60.0)
    ap.add_argument("-i", "--interval", type=float, default=0.5)
    ap.add_argument("--expect", type=int, help="required HTTP status code")
    ap.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args(argv)

    for target in args.targets:
        check, label = make_check(target, args.expect)
        if not args.quiet:
            print("waiting for %s (up to %gs)" % (label, args.timeout), file=sys.stderr)
        elapsed = wait(check, args.timeout, args.interval)
        if elapsed is None:
            print("timed out waiting for %s" % label, file=sys.stderr)
            return 1
        if not args.quiet:
            print("%s ready in %.1fs" % (label, elapsed), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
