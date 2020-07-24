import json
import logging
import os
import socket
import sys
import threading
import time

import pytest
from flask import Flask, g, session

from app import create_app


class StreamToLogger(object):
    """
   Fake file-like stream object that redirects writes to a logger instance.
   Not actually used by tests, but if the tests fail the logger messages from the flask
   server thread are output to the out.log file, which is super handy
   """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ""

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    filename="out.log",
    filemode="a",
)

stdout_logger = logging.getLogger("STDOUT")
sl = StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl

stderr_logger = logging.getLogger("STDERR")
sl = StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl


def get_open_port():
    """ Find free port on a local system """
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(("", 0))
    # port = s.getsockname()[1]
    # s.close()
    # return port
    return 57244


def wait_until(predicate, timeout=5, interval=0.05, *args, **kwargs):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if predicate(*args, **kwargs):
            return True
        time.sleep(interval)
    return False



@pytest.fixture(scope="session")
def test_server():


    http_server = create_app(test_config="banana")
    routes = [str(p) for p in http_server.url_map.iter_rules()]
    print(f"routes: {routes}")

    port = get_open_port()
    http_server.url = f"http://localhost:{port}"
    print(f"http_server.url: {http_server.url}")
    http_server.schema_url = f"{http_server.url}/static/schema.json"


    def start():
        print("start server")
        http_server.run(port=port)

    p = threading.Thread(target=start)
    p.daemon = True
    p.start()

    def check():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(("localhost", port))
            return True
        except Exception:
            return False
        finally:
            s.close()

    rc = wait_until(check)
    assert rc, "failed to start service"



    yield http_server

    p.join(timeout=0.5)



