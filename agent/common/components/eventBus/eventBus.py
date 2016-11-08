from logging import getLogger
from asyncio import Queue, ensure_future, gather

log = getLogger()


class Event:
    def __init__(self, name, data):
        self.name = name
        self.data = data


class Channel:
    """Holds messages for an Event in Bus"""
    def __init__(self):
        """Creates a Channel which has it's own queue of messages"""
        self._queue = Queue()

    async def __aiter__(self):
        return self

    async def __anext__(self):
        data = await self._queue.get()
        self._queue.task_done()

        if data == 'STOP':
            raise StopAsyncIteration

        return data

    async def put(self, data):
        await self._queue.put(data)


class Bus:
    """Broker and a client which allows to create a pub/sub model"""
    def __init__(self):
        self._events = {}

    def subscribe(self, eventName):
        """
        Subscribe to a channel and listen for messages on returned channel
        :param eventName: Name of event on which to listen for messages
        :return: Channel on which we will publish messages for subscribed event
        """
        if eventName not in self._events:
            self._events[eventName] = set()
            log.debug('No event found on bus with name "{}"'.format(eventName))
            log.debug('Created listener set for above event')
        # May be get it from Channel Pool
        channel = Channel()
        self._events[eventName].add(channel)
        log.debug('subscribed to {}'.format(eventName))

        return channel

    async def unsubscribe(self, eventName, channel):
        """
        Removes a channel from subscribers, and deletes that channel
        :param eventName: name with which to remove the channel
        :param channel: Instance of Channel class to remove
        :return: void
        """
        if eventName in self._events:
            if channel in self._events[eventName]:
                self._events[eventName].remove(channel)
                log.debug('unsubcribed {} from {}'.format(channel, eventName))
                # special signal to stop processing events and close async for
                await channel.put('STOP')
                del channel
                log.debug('deleted channel object')
            else:
                log.debug(
                    'No channel to unsubscribe on event: {}'.format(eventName)
                )
        else:
            log.debug(
                'No event with name as "{}" found on bus'.format(eventName)
            )

    async def publish(self, eventName, data):
        """Send event data to every channel subscribed to this event
        :param eventName: Name of the event
        :param data: Data to send to all subscribers
        :return: void
        """
        if eventName in self._events:
            event = Event(eventName, data)
            tasks = []
            for channel in self._events[eventName]:
                tasks.append(ensure_future(channel.put(event)))

            log.debug('publishing event to {} channels'.format(len(tasks)))
            log.debug(
                'published event "{}" on bus with data "{}"'.format(
                    eventName, data
                )
            )
            # May be we can just gather and don't await here
            await gather(*tasks)

# ensure that there should be only one bus
"""Single bus instance to be used throughout the project"""
bus = Bus()
