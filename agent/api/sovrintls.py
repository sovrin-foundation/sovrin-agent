
import aiohttp
import asyncio
import json

postData = {
    'route': 'acceptInvitation',
    'signature': '979nknksdnknkskdsha797979878',
    'sovrinId': 'sovrinId',
    'invitation': {
        'id': '3W2465HP3OUPGkiNlTMl2iZ+NiMZegfUFIsl8378KH4=',
        'publicKey': 'adfasdfuyaddfiaifd8f8d6f8df764svua',
        'signature': 'oiadmmat0-tvknaai7efa7f5aklfaf=adf8ff'
    }
}


async def acceptInvitation(client):
    async with client.post('http://localhost:8080/acceptInvitation', data=json.dumps(postData)) as resp:
        #assert resp.status == 200
        return await resp.text()

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as client:
        html = await acceptInvitation(client)
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))