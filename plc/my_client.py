from asyncua import Client, ua


class PLCClient:
    def __init__(self, url):
        self.url = url
        self.client = Client(url=url)
        self.connected = False

    async def connect(self):
        try:
            await self.client.connect()
            self.connected = True
            print("Connected to PLC")
        except Exception as e:
            print(f"Error connecting to PLC: {e}")
            self.connected = False

    async def disconnect(self):
        if self.connected:
            await self.client.disconnect()
            self.connected = False
            print("Disconnected from PLC")

    async def read_node(self, node_id):
        if self.connected:
            try:
                node = self.client.get_node(node_id)
                value = await node.read_value()
                return value
            except Exception as e:
                print(f"Error reading node {node_id}: {e}")
                return None
        else:
            # print("Not connected to PLC (1)")
            return None

    async def write_node(self, node_id, value):
        if self.connected:
            try:
                node = self.client.get_node(node_id)
                variant = ua.Variant(value, ua.VariantType.Boolean)
                data_value = ua.DataValue(variant)
                await node.write_value(data_value)
                print(f"Written value {value} to node {node_id}")
            except Exception as e:
                print(f"Error writing to node {node_id}: {e}")
        else:
            print("Not connected to PLC(2)")

    async def browse(self, node_id):
        if self.connected:
            try:
                node = self.client.get_node(node_id)
                children = await node.get_children()
                return children
            except Exception as e:
                print(f"Error browsing node {node_id}: {e}")
                return None
        else:
            print("Not connected to PLC(3)")
            return None

    async def toggle_output(self, node_id):
        # Read the current value of the node
        current_value = await self.read_node(node_id)
        # Toggle the value
        new_value = not current_value
        # Write the new value to the node
        await self.write_node(node_id, new_value)
