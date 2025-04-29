# opcua/nodes.py

NODE_ADDRESSES = {
    # INPUTS
    "i00": "ns=4;i=16",
    "i01": "ns=4;i=17",
    "i02": "ns=4;i=18",
    "i03": "ns=4;i=19",
    "i04": "ns=4;i=20",
    "i05": "ns=4;i=21",
    "i06": "ns=4;i=22",
    "i07": "ns=4;i=23",
    "i10": "ns=4;i=24",
    "i11": "ns=4;i=25",
    "i12": "ns=4;i=26",
    "i13": "ns=4;i=27",
    "i14": "ns=4;i=28",
    "i15": "ns=4;i=29",

    # OUTPUTS
    "o00": "ns=4;i=5",
    "o01": "ns=4;i=6",
    "o02": "ns=4;i=7",
    "o03": "ns=4;i=8",
    "o04": "ns=4;i=9",
    "o05": "ns=4;i=10",
    "o06": "ns=4;i=11",
    "o07": "ns=4;i=12",
    "o10": "ns=4;i=13",
    "o11": "ns=4;i=14",

    # MEMORY
}


async def get_node_value(client, node_name):
    """Read the value from a node by name."""
    if node_name not in NODE_ADDRESSES:
        raise ValueError(f"Node '{node_name}' not found!")

    node_address = NODE_ADDRESSES[node_name]
    node = await client.nodes.objects.get_child([node_address])
    return await node.read_value()


async def write_node_value(client, node_name, value):
    """Write a value to a node by name."""
    if node_name not in NODE_ADDRESSES:
        raise ValueError(f"Node '{node_name}' not found!")

    node_address = NODE_ADDRESSES[node_name]
    node = await client.nodes.objects.get_child([node_address])
    await node.write_value(value)
