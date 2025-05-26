import asyncio
from plc.my_nodes import io_addresses


async def run_sequence(plc):
    try:
        # Get addresses
        q00 = io_addresses.get("Q00")
        q01 = io_addresses.get("Q01")
        q02 = io_addresses.get("Q02")
        q03 = io_addresses.get("Q03")
        q04 = io_addresses.get("Q04")
        q05 = io_addresses.get("Q05")
        q06 = io_addresses.get("Q06")
        q07 = io_addresses.get("Q07")
        q10 = io_addresses.get("Q10")
        q11 = io_addresses.get("Q11")

        i00 = io_addresses.get("I00")
        i01 = io_addresses.get("I01")
        i02 = io_addresses.get("I02")
        i03 = io_addresses.get("I03")
        i04 = io_addresses.get("I04")
        i05 = io_addresses.get("I05")
        i06 = io_addresses.get("I06")
        i07 = io_addresses.get("I07")
        i10 = io_addresses.get("I10")
        i11 = io_addresses.get("I11")

        # Validate required addresses
        if not all([q00, q01, q02, q03, q04, q05, q06, q07, q10, q11, i00, i01, i02, i03, i04, i05, i06, i07, i10, i11]):
            print("Required I/O addresses not found in io_addresses.")
            return

        print("Waiting for input I00 to become True...")

        # Wait until input I00 becomes True
        while True:
            input_state = await plc.read_node(i00)
            if input_state:
                break
            await asyncio.sleep(0.1)

        print("Input I00 is active. E.Stop engaged")

        while True:
            input_state = await plc.read_node(i01)
            if input_state:
                break
            await asyncio.sleep(0.1)

        for i in range(2):
            await plc.write_node(q00, True)
            await asyncio.sleep(0.01)
            await plc.write_node(q00, False)
            await asyncio.sleep(0.01)
            await plc.write_node(q01, True)
            await asyncio.sleep(0.01)
            await plc.write_node(q01, False)
            await asyncio.sleep(0.01)
            await plc.write_node(q02, True)
            await asyncio.sleep(0.01)
            await plc.write_node(q02, False)
            await asyncio.sleep(0.01)
            await plc.write_node(q03, True)
            await asyncio.sleep(0.01)
            await plc.write_node(q03, False)
            await asyncio.sleep(0.01)
            await plc.write_node(q04, True)
            await asyncio.sleep(0.01)
            await plc.write_node(q04, False)
            await asyncio.sleep(0.01)
            await plc.write_node(q05, True)
            await asyncio.sleep(0.01)
            await plc.write_node(q05, False)
            await asyncio.sleep(0.01)
            await plc.write_node(q06, True)
            await asyncio.sleep(0.01)
            await plc.write_node(q06, False)
            await asyncio.sleep(0.01)
            await plc.write_node(q07, True)
            await asyncio.sleep(0.01)
            await plc.write_node(q07, False)
            await asyncio.sleep(0.01)
            await plc.write_node(q10, True)
            await asyncio.sleep(0.01)
            await plc.write_node(q10, False)
            await asyncio.sleep(0.01)
            await plc.write_node(q11, True)
            await asyncio.sleep(0.01)
            await plc.write_node(q11, False)
            await asyncio.sleep(0.01)

        print("Sequence input_output finished.")
    except Exception as e:
        print(f"Error in run_sequence: {e}")
