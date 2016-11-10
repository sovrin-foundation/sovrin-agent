import logging
import pytest

from inspect import stack
from asyncio import ensure_future, gather, sleep
from unittest.mock import Mock, call

from agent.common.components.eventBus.eventBus import bus


@pytest.fixture
def log():
    return logging.getLogger()


@pytest.fixture
def eventName():
    return 'test'


@pytest.fixture
def eventData():
    return 'Dummy text data to publish'


@pytest.mark.asyncio
async def testSubscribeCallsDataForEachChannel(
        log,
        eventName,
        eventData):

    log.debug = Mock(wraps=log.debug)

    async def subscriber():
        testChannel = bus.subscribe(eventName)
        callableName = stack()[1][3]
        async for testEvent in testChannel:
            log.debug('Called {}'.format(callableName))
            assert testEvent.data == eventData
            await bus.unsubscribe(eventName, testChannel)
        else:
            log.debug('Stopped channel of method {}'.format(callableName))

    async def subscriber1():
        await subscriber()

    async def subscriber2():
        await subscriber()

    tasks = [
        ensure_future(subscriber1()),
        ensure_future(subscriber2())
    ]
    # Let event loop run above tasks
    await sleep(0)
    # Now publish, once we have subscribed to bus
    await bus.publish(eventName, eventData)
    await gather(*tasks)
    # Verify that logs were called in subscribers as well
    logCalls = [
        call('Called subscriber1'),
        call('Called subscriber2'),
        call('Stopped channel of method subscriber1'),
        call('Stopped channel of method subscriber2')
    ]
    log.debug.assert_has_calls(logCalls, any_order=True)
    log.debug.reset_mock()


@pytest.mark.asyncio
async def testUnsubscribeRemovesChannelFromPublish(
    log,
    eventName,
    eventData
):
    log.debug = Mock(wraps=log.debug)
    testChannel = bus.subscribe(eventName)

    async def testSubscriber():
        async for testEvent in testChannel:
            log.debug(
                'Received Event on test Channel with {}'.format(testEvent.data)
            )
        else:
            log.debug('Closed test channel')

    # Run subscriber, so that it starts waiting for a message
    subscriberTask = ensure_future(testSubscriber())
    await sleep(0)
    await bus.unsubscribe(eventName, testChannel)
    await bus.publish(eventName, eventData)
    await subscriberTask
    # log should not have any call with text as data received
    unexpectedLog = 'Received Event on test Channel with {}'\
        .format(eventData)
    assert (unexpectedLog,) not in log.debug.mock_calls
    log.debug.reset_mock()
