# opcua/client.py

from asyncua import Client


class PLCClient:
    def __init__(self, url):
        self.url = url
        self.client = Client(url)

    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    def get_client(self):
        return self.client
