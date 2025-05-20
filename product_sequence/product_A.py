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
        i00 = io_addresses.get("I00")
        i01 = io_addresses.get("I01")

        # Validate required addresses
        if not all([q00, q01, i00]):
            print("Required I/O addresses not found in io_addresses.")
            return

        print("Waiting for input I00 to become True...")

        # Wait until input I00 becomes True
        while True:
            input_state = await plc.read_node(i00)
            if input_state:
                break
            await asyncio.sleep(0.1)  # avoid tight loop

        print("Input I00 is active. E.Stop engaged")

        while True:
            input_state = await plc.read_node(i01)
            if input_state:
                break
            await asyncio.sleep(0.1)  # avoid tight loop

        # Run output sequence
        await plc.write_node(q01, True)
        await asyncio.sleep(1)
        await plc.write_node(q02, True)
        await asyncio.sleep(1)
        await plc.write_node(q03, True)
        await asyncio.sleep(1)
        await plc.write_node(q04, True)
        await asyncio.sleep(1)
        await plc.write_node(q05, True)
        await plc.write_node(q00, False)
        await plc.write_node(q01, False)
        await plc.write_node(q02, False)
        await plc.write_node(q03, False)
        await plc.write_node(q04, False)
        await plc.write_node(q05, False)
        print("Sequence A finished.")

    except Exception as e:
        print(f"Error in run_sequence: {e}")
