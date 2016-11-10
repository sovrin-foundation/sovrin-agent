## Using event bus
`from agent.common.components.eventBus import bus`
Above statement will utilise a single bus instance throughout the project.
If you need to create new instances of a bus and use it only in a specific
module, then create an instance of `Bus` class.

## Subscribing and using a channel
```
from agent.common.components.eventBus import bus

loginChannel = bus.subscribe('login-successful')
async for event in loginChannel:
    websocket.send(event.data)
else:
    log.debug('No message on channel')
```

## Unsubscribe to a channel
`bus.unsubscribe(eventName='login-successful', channel=loginChannel)`

## Publish data on a channel
`bus.publish('login-successful', data={'sovrinId': 'a'})`

## API
Start an API server using command give below and click on agent
`pydoc -b -p 1234 agent.common.components.eventBus.eventBus`
