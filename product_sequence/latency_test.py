import asyncio
from plc.my_nodes import io_addresses


async def run_sequence(plc):
    try:
        # Get addresses
        q00 = io_addresses.get("Q00")
        i00 = io_addresses.get("I00")

        # Validate required addresses
        if not all([q00, i00]):
            print("Required I/O addresses not found in io_addresses.")
            return

        print("Waiting for input I00 to become True...")

        # Continuously monitor input I00
        while True:
            input_state = await plc.read_node(i00)

            if input_state:
                await plc.write_node(q00, True)
                print("Input I00 detected. Output Q00 activated.")
                await plc.write_node(q00, False)
                break

            await asyncio.sleep(0.1)

    except Exception as e:
        print(f"An error occurred: {e}")
