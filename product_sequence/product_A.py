import asyncio
from plc.my_nodes import io_addresses


async def run_sequence(plc):
    try:
        plc.running = True

        q00 = io_addresses.get("Q00")
        q01 = io_addresses.get("Q01")
        q02 = io_addresses.get("Q02")
        q03 = io_addresses.get("Q03")
        q04 = io_addresses.get("Q04")
        q05 = io_addresses.get("Q05")
        i00 = io_addresses.get("I00")
        i01 = io_addresses.get("I01")

        if not all([q00, q01, i00]):
            print("Required I/O addresses not found.")
            return

        print("Waiting for input I00 to become True...")

        while plc.running:
            if await plc.read_node(i00):
                break
            await asyncio.sleep(0.1)

        if not plc.running:
            print("Sequence A stopped before start.")
            return

        print("I00 active. Waiting for I01...")

        while plc.running:
            if await plc.read_node(i01):
                break
            await asyncio.sleep(0.1)

        if not plc.running:
            print("Sequence A stopped before output phase.")
            return

        for node in [q01, q02, q03, q04, q05]:
            if not plc.running:
                print("Sequence A interrupted during output.")
                return
            await plc.write_node(node, True)
            await asyncio.sleep(1)

        for node in [q00, q01, q02, q03, q04, q05]:
            await plc.write_node(node, False)

        print("Sequence A finished.")

    except Exception as e:
        print(f"Error in run_sequence: {e}")


async def stop_sequence(plc):
    plc.running = False
    print("Stopping product A.")


async def reset_sequence(plc):
    try:
        await stop_sequence(plc)
        print("Resetting product A sequence...")

        # Turn off outputs
        for key in ["Q00", "Q01", "Q02", "Q03", "Q04", "Q05"]:
            node = io_addresses.get(key)
            if node:
                await plc.write_node(node, False)

        # Optionally reset internal state or flags
        plc.running = False

        print("Reset complete.")

    except Exception as e:
        print(f"Error in reset_sequence: {e}")
