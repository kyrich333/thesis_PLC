from asyncua import Client
import asyncio

url = "opc.tcp://192.168.0.1:4840"
io_addresses = {
    # INPUTS
    "I00": "ns=4;i=16",
    "I01": "ns=4;i=17",
    "I02": "ns=4;i=18",
    "I03": "ns=4;i=19",
    "I04": "ns=4;i=20",
    "I05": "ns=4;i=21",
    "I06": "ns=4;i=22",
    "I07": "ns=4;i=23",
    "I10": "ns=4;i=24",
    "I11": "ns=4;i=25",
    "I12": "ns=4;i=26",
    "I13": "ns=4;i=27",
    "I14": "ns=4;i=28",
    "I15": "ns=4;i=29",

    # OUTPUTS
    "Q00": "ns=4;i=5",
    "Q01": "ns=4;i=6",
    "Q02": "ns=4;i=7",
    "Q03": "ns=4;i=8",
    "Q04": "ns=4;i=9",
    "Q05": "ns=4;i=10",
    "Q06": "ns=4;i=11",
    "Q07": "ns=4;i=12",
    "Q10": "ns=4;i=13",
    "Q11": "ns=4;i=14",
}

io_state = {

    # INPUTS
    "I00": False,
    "I01": False,
    "I02": False,
    "I03": False,
    "I04": False,
    "I05": False,
    "I06": False,
    "I07": False,
    "I10": False,
    "I11": False,
    "I12": False,
    "I13": False,
    "I14": False,
    "I15": False,

    # OUTPUTS
    "Q00": False,
    "Q01": False,
    "Q02": False,
    "Q03": False,
    "Q04": False,
    "Q05": False,
    "Q06": False,
    "Q07": False,
    "Q10": False,
    "Q11": False,
}
