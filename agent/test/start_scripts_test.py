import os
from _signal import SIGINT
from subprocess import Popen
from sys import executable
from time import sleep


def test_startApiServer():
    port_range_end = 8090 # XXX
    for port in range(8080, port_range_end):
        res = run_script('startApiServer', '0.0.0.0', str(port))
        try:
            assert res == 0, 'script failed'
        except AssertionError:
            if res != 2 or port == port_range_end: # 2 means address in use
                raise
        else:
            return


def run_script(script, *args):
    s = os.path.join(os.path.dirname(__file__), '../../scripts/' + script)
    command = [executable, s]
    command.extend(args)

    with Popen(command, env={'PYTHONPATH': '.'}) as p:
        sleep(4)
        p.send_signal(SIGINT)
        p.wait(timeout=1)
        return p.poll()

