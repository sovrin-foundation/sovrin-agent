import os
from _signal import SIGINT
from subprocess import Popen
from sys import executable
from time import sleep


def test_startApiServer():
    run_script('startApiServer')


def run_script(script, *args):
    s = os.path.join(os.path.dirname(__file__), '../../scripts/' + script)
    command = [executable, s]
    command.extend(args)

    with Popen([executable, s]) as p:
        sleep(2)
        p.send_signal(SIGINT)
        p.wait(timeout=1)
        assert p.poll() == 0, 'script failed'

