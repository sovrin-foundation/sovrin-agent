import os
from _signal import SIGINT
from subprocess import Popen
from sys import executable
from time import sleep


def test_startApiServer():
    for port in range(8080, 8090): # try several ports to find the free one
        res = run_script('startApiServer', '0.0.0.0', str(port))
        if res != 2: # 2 means address in use
            break

    assert res == 0, 'script failed'


def run_script(script, *args):
    s = os.path.join(os.path.dirname(__file__), '../../scripts/' + script)
    command = [executable, s]
    command.extend(args)

    with Popen(command, env={'PYTHONPATH': '.'}) as p:
        sleep(4)
        p.send_signal(SIGINT)
        p.wait(timeout=1)
        return p.poll()

