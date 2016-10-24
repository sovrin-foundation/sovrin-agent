from asyncio import get_event_loop, sleep
from pytest import fixture, mark
from agent.agent import Agent
from plenum.common.startable import Status


@fixture()
def loop():
    return get_event_loop()


@fixture()
def agent():
    return Agent()


@mark.asyncio
async def testStartup(agent, loop):
    # TODO: Why is OrientDB starting up???
    # TODO: Why is a node set startup up???
    agent.start(loop)
    assert agent.isGoing() is True
    assert agent.get_status() is Status.starting
    await sleep(0.01)
    # TODO: Understand what is the parameter we are passing in prod
    await agent.prod(1)
    assert agent.get_status() is Status.started


def testShutdown(agent):
    agent.stop()
    assert agent.isGoing() is False
    assert agent.get_status() is Status.stopped
