import asyncio
import threading
import time
from tkinter import Tk, ttk, Canvas
from plc.my_client import PLCClient
from plc.nodes import NODE_ADDRESSES  # Import the NODE_ADDRESSES dictionary


class PLCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PLC Controller")
        self.root.geometry("1920x1280")

        self.loop = asyncio.new_event_loop()
        self.plc = PLCClient("opc.tcp://192.168.0.1:4840")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.node_id_mapping = {}  # Store Node IDs for each LED
        self.create_home_tab()
        self.create_tools_tab()
        self.create_sequence_edit_tab()

    def create_home_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Home")
        tab.grid_rowconfigure((0, 1), weight=1)
        tab.grid_columnconfigure((0), weight=1)

        frame_up = ttk.Frame(tab, borderwidth=2, relief="groove")
        frame_up.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_up, text="Top Left Content").pack(padx=10, pady=10)

        frame_lo = ttk.Frame(tab, borderwidth=2, relief="groove")
        frame_lo.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_lo, text="Bottom Left Content").pack(padx=10, pady=10)

    def create_tools_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Tools")
        tab.grid_rowconfigure((0, 1, 2, 3), weight=1)
        tab.grid_columnconfigure((0), weight=1)

        # Input Section
        upper_title = ttk.Label(tab, text="Inputs")
        upper_title.grid(row=0, column=0, padx=1, pady=1)
        upper_section = ttk.Frame(tab, borderwidth=2, relief="groove")
        upper_section.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self._create_io_elements(
            upper_section, "I", range(2), range(8), add_led=True)

        # Output Section
        lower_title = ttk.Label(tab, text="Outputs")
        lower_title.grid(row=2, column=0, padx=1, pady=1)
        lower_section = ttk.Frame(tab, borderwidth=2, relief="groove")
        lower_section.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self._create_io_elements(
            lower_section, "O", range(2), range(5), add_led=True)

    def _create_io_elements(
        self, parent_frame, io_type, row_range, col_range, add_led=False
    ):
        for row_index in row_range:
            parent_frame.grid_rowconfigure(row_index, weight=1)
        for col_index in col_range:
            parent_frame.grid_columnconfigure(col_index, weight=1)
        for row_index in row_range:
            for col_index in col_range:
                frame = ttk.Frame(parent_frame, borderwidth=2, relief="groove")
                frame.grid(row=row_index, column=col_index,
                           sticky="nsew", padx=5, pady=5)
                label_text = f"{io_type} {row_index}.{col_index}"
                ttk.Label(frame, text=label_text).pack(padx=10, pady=10)

                if add_led:
                    # Create a Canvas for the LED
                    led_canvas = Canvas(frame, width=16, height=16, bg="white")
                    led_canvas.pack(padx=5, pady=5)
                    frame.led_canvas = led_canvas
                    frame.led_circle = led_canvas.create_oval(
                        2, 2, 14, 14, fill="gray", outline=""
                    )
                    frame.io_type = io_type
                    frame.io_address = (row_index, col_index)

                    # **Crucial:** Assign Node ID here, using the dictionary from plc/nodes.py
                    # Construct the key
                    key = f"{io_type.lower()}{row_index}{col_index}"
                    if key in NODE_ADDRESSES:
                        node_id = NODE_ADDRESSES[key]
                        self.node_id_mapping[(
                            io_type, row_index, col_index)] = node_id
                    else:
                        print(
                            f"Warning: Node ID for {key} not found in NODE_ADDRESSES"
                        )
                        # Handle the error, e.g., set a default Node ID or skip the LED
                        self.node_id_mapping[
                            (io_type, row_index, col_index)
                        ] = None  # important:  set it to none rather than some random string

    def create_sequence_edit_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Sequence Edit")
        tab.grid_rowconfigure((0, 1, 2), weight=1)
        tab.grid_columnconfigure((0, 1), weight=1)

    def update_led(self, io_type, address, value):
        """Updates the LED color based on the given IO type, address, and value."""
        for child in self.notebook.winfo_children():
            if child.winfo_name() == "Tools":
                for section_child in child.winfo_children():
                    if isinstance(section_child, ttk.Frame):
                        for frame_child in section_child.winfo_children():
                            if (
                                hasattr(frame_child, "io_type")
                                and hasattr(frame_child, "io_address")
                            ):
                                if (
                                    frame_child.io_type == io_type
                                    and frame_child.io_address == address
                                ):
                                    led_canvas = frame_child.led_canvas
                                    led_color = "green" if value else "gray"
                                    led_canvas.itemconfig(
                                        frame_child.led_circle, fill=led_color
                                    )
                                    return
        print(
            f"LED with type {io_type} and address {address} not found"
        )  # Error Handling

    async def read_plc_values(self):
        """
        Reads values from the PLC and updates the LEDs.  This function runs in the asyncio loop.
        """
        while True:
            if not self.plc.connected:
                print("Waiting for PLC to connect...")
                await asyncio.sleep(1)  # Wait and check again
                continue  # Skip the rest of the loop and try again

            for (
                io_type,
                row_index,
                col_index,
            ), node_id in self.node_id_mapping.items():
                if node_id is not None:  # only read if node_id is not None
                    try:
                        value = await self.plc.read_node(
                            node_id
                        )  # Read from PLC
                        if value is not None:
                            self.update_led(
                                io_type, (row_index, col_index), value
                            )  # Update LED color
                    except Exception as e:
                        print(f"Error reading from PLC: {e}")
                        # Consider if you want to attempt a reconnect here.
                await asyncio.sleep(
                    0.1
                    # Add a small delay to prevent overwhelming the PLC.  Adjust as needed.
                )
            await asyncio.sleep(1)  # Read all values every second

    async def close_plc_connection(self):
        """Close the PLC connection when the application exits."""
        if self.plc.connected:
            await self.plc.disconnect()

    def __del__(self):
        """Ensure the PLC connection is closed when the object is destroyed."""
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(
                asyncio.run_coroutine_threadsafe,
                self.close_plc_connection(),
                self.loop,
            )  # use call_soon_threadsafe


def main():
    root = Tk()
    app = PLCApp(root)

    async def run_app():
        try:
            # Ensure the PLC connection is established before proceeding
            await app.plc.connect()
            print("PLC Connected. Starting GUI and data updates.")
            # Start the data reading loop in the asyncio event loop
            # Start read_plc_values as a background task
            asyncio.create_task(app.read_plc_values())
        except Exception as e:
            # Handle errors during connect or read
            print(f"An error occurred: {e}")
        # finally: # Removed:  Moved to __del__
        #    await app.close_plc_connection()

    # Run the asyncio event loop in a separate thread
    loop_thread = threading.Thread(
        target=start_asyncio_loop, args=(app.loop, run_app))
    loop_thread.daemon = True  # Allow the program to exit even if this thread is running
    loop_thread.start()

    root.mainloop()  # Start the Tkinter main loop (this needs to be done in the main thread)


def start_asyncio_loop(loop, run_app):
    """Start the asyncio loop and run the run_app function."""
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_app())
    loop.close()
