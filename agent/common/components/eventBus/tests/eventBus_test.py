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
def testChannelName():
    return 'test'


@pytest.fixture
def testChannelData():
    return 'Dummy text data to publish'


@pytest.mark.asyncio
async def test_subscribeCallsDataForEachChannel(
        log,
        testChannelName,
        testChannelData):

    log.debug = Mock(wraps=log.debug)

    async def testMethod1():
        testChannel = bus.subscribe(testChannelName)
        callableName = stack()[0][3]
        async for testEvent in testChannel:
            log.debug('Called {}'.format(callableName))
            assert testEvent.data == testChannelData
            await bus.unsubscribe(testChannelName, testChannel)
        else:
            log.debug('Stopped channel of method {}'.format(callableName))

    async def testMethod2():
        testChannel = bus.subscribe(testChannelName)
        callableName = stack()[0][3]
        async for testEvent in testChannel:
            log.debug('Called {}'.format(callableName))
            assert testEvent.data == testChannelData
            await bus.unsubscribe(testChannelName, testChannel)
        else:
            log.debug('Stopped channel of method {}'.format(callableName))

    tasks = [
        ensure_future(testMethod1()),
        ensure_future(testMethod2())
    ]
    # Let event loop run above tasks
    await sleep(0)
    # Now publish, once we have subscribed to bus
    await bus.publish(testChannelName, testChannelData)
    await gather(*tasks)
    # Verify that logs were called in subscribers as well
    logCalls = [
        call('Called testMethod1'),
        call('Called testMethod2'),
        call('Stopped channel of method testMethod1'),
        call('Stopped channel of method testMethod2')
    ]
    log.debug.assert_has_calls(logCalls, any_order=True)
    log.debug.reset_mock()


@pytest.mark.asyncio
async def test_unsubscribeRemovesChannelFromPublish(
    log,
    testChannelName,
    testChannelData
):
    log.debug = Mock(wraps=log.debug)
    testChannel = bus.subscribe(testChannelName)

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
    await bus.unsubscribe(testChannelName, testChannel)
    await bus.publish(testChannelName, testChannelData)
    await subscriberTask
    # log should not have any call with text as data received
    unexpectedLog = 'Received Event on test Channel with {}'\
        .format(testChannelData)
    assert (unexpectedLog,) not in log.debug.mock_calls
    log.debug.reset_mock()
