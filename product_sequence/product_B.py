import asyncio
from plc.my_nodes import io_addresses


async def run_sequence(plc):
    try:
        # Get addresses
        q00 = io_addresses.get("Q00")
        q01 = io_addresses.get("Q02")
        i00 = io_addresses.get("I00")

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

        print("Input I00 is active. Running sequence...")

        # Run output sequence

        await plc.write_node(q00, True)
        await asyncio.sleep(0.1)
        await plc.write_node(q00, False)
        await plc.write_node(q01, True)
        await asyncio.sleep(1)
        await plc.write_node(q01, False)
        await plc.write_node(q00, False)

        print("Sequence B finished.")

    except Exception as e:
        print(f"Error in run_sequence: {e}")
