import asyncio
import threading
import importlib
import os
from tkinter import Tk, ttk, Button, Label, Canvas, StringVar
from plc.my_client import PLCClient
from plc.my_nodes import io_addresses, io_state

product_sequence_folder = '/home/richky/thesis_app/product_sequence'


class AsyncioLoopThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.loop = asyncio.new_event_loop()

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()


class PLCApp:
    def __init__(self, root, asyncio_thread):
        self.root = root
        self.root.title("PLC_Controller")
        self.root.geometry("1920x1080")

        # asynchronous setup
        self.asyncio_thread = asyncio_thread
        self.loop = asyncio_thread.loop  # Use the existing running event loop

        self.plc = PLCClient("opc.tcp://192.168.0.1:4840")
        asyncio.run_coroutine_threadsafe(self.plc.connect(), self.loop)
        asyncio.run_coroutine_threadsafe(self.monitor_io_states(), self.loop)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)
        self.node_addresses = io_addresses
        self.io_states = io_state
        self.selected_sequence = StringVar()

        self.create_tabs()

    def list_files_in_directory(self, directory):
        # List all files in the directory
        return os.listdir(directory)

    def update_combobox(self):
        # Get the files from the product sequence folder
        files = self.list_files_in_directory(product_sequence_folder)
        # Update the combobox with file names
        files = [
            f[:-3] for f in files if f.endswith('.py') and not f.startswith('__pycache__')
        ]
        self.sequence_combobox['values'] = files
        if files:
            self.selected_sequence.set(files[0])

    def send_to_client(self, key):
        node_address = self.node_addresses.get(key)
        if node_address:
            asyncio.run_coroutine_threadsafe(
                self.plc.toggle_output(node_address), self.loop)
            print(f"Sent command to PLC: {node_address}")
        else:
            print(f"Node ID {key} send to client.")

    async def get_from_client(self, key):
        node_address = self.node_addresses.get(key)
        if node_address:
            try:
                node_value = await self.plc.read_node(node_address)
                return node_value

            except Exception as e:
                print(f"Error reading node {node_address}: {e}")
        else:
            print(
                f"Node ID {key} not found in node_addresses <get_from_client>.")

    def change_widget_color(self, key):
        widget_value = self.io_states.get(key)

        def apply_color():
            widget = self.widget_addresses.get(key)
            if widget:
                if widget_value is True:
                    widget.config(bg="green")
                elif widget_value is False:
                    widget.config(bg="red")
                else:
                    print(f"Invalid widget value for {key}: {widget_value}")
            else:
                print(f"Widget not found for key: {key}")

        self.root.after(0, apply_color)

    def handle_button_click(self, key):
        self.send_to_client(key)
        asyncio.run_coroutine_threadsafe(self.update_io_states(key), self.loop)

    async def update_io_states(self, key):
        node_value = await self.get_from_client(key)
        if key in self.io_states:
            if self.io_states[key] != node_value:
                self.io_states[key] = node_value
                print(f"Updated {key} state to {node_value}")
                self.change_widget_color(key)

    async def monitor_io_states(self):
        while True:
            tasks = [self.update_io_states(key)
                     for key in self.io_states.keys()]
            await asyncio.gather(*tasks)
            await asyncio.sleep(0.025)  # Adjust the sleep time as needed

    def run_selected_sequence(self, sequence_name):
        try:
            module = importlib.import_module(
                f"product_sequence.{sequence_name}")
            asyncio.run_coroutine_threadsafe(
                module.run_sequence(self.plc), self.loop
            )
            print(f"Running sequence: {sequence_name}")
        except Exception as e:
            print(f"Failed to run sequence {sequence_name}: {e}")

    def create_tabs(self):
        # Home Tab
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Home")
        tab1.grid_rowconfigure((0, 1), weight=1)
        tab1.grid_columnconfigure((0), weight=1)

        frame_up = ttk.Frame(tab1, borderwidth=2, relief="groove")
        frame_up.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame_up.grid_columnconfigure((0, 1), weight=1)
        frame_up.grid_rowconfigure((0), weight=1)

        frame_up_left = ttk.Frame(frame_up, borderwidth=2, relief="groove")
        frame_up_left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        Label(frame_up_left, text="On going : ").grid(padx=10, pady=10)

        self.sequence_combobox = ttk.Combobox(
            frame_up_left, textvariable=self.selected_sequence)
        self.sequence_combobox.grid(row=0, column=2)

        self.update_combobox()

        button_start = Button(frame_up_left, padx=40, pady=20, bg="grey", text="start",
                              command=lambda: self.run_selected_sequence(self.selected_sequence.get()))
        button_start.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)

        frame_up_right = ttk.Frame(frame_up, borderwidth=2, relief="groove")
        frame_up_right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        Label(frame_up_right, text="Queue : ").grid(padx=10, pady=10)

        frame_lo = ttk.Frame(tab1, borderwidth=2, relief="groove")
        frame_lo.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        Label(frame_lo, text="lower section").grid(padx=10, pady=10)

        # Tools Tab
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Tools")
        tab2.grid_rowconfigure((0, 1, 2, 3), weight=1)
        tab2.grid_columnconfigure((0), weight=1)

        # upper section tools tab
        upper_title = Label(tab2, text="Inputs")
        upper_title.grid(row=0, column=0, padx=1, pady=1)
        upper_section = ttk.Frame(tab2, borderwidth=2, relief="groove")
        upper_section.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        upper_section.grid_rowconfigure((0, 1), weight=1)
        upper_section.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        frame_I00 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I00.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame_I00.grid_columnconfigure((0), weight=1)
        frame_I00.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I00, text="I 0.0").grid(padx=10, pady=10,)

        frame_I01 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I01.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        frame_I01.grid_columnconfigure((0), weight=1)
        frame_I01.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I01, text="I 0.1").grid(padx=10, pady=10)

        frame_I02 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I02.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        frame_I02.grid_columnconfigure((0), weight=1)
        frame_I02.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I02, text="I 0.2").grid(padx=10, pady=10)

        frame_I03 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I03.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        frame_I03.grid_columnconfigure((0), weight=1)
        frame_I03.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I03, text="I 0.3").grid(padx=10, pady=10)

        frame_I04 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I04.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)
        frame_I04.grid_columnconfigure((0), weight=1)
        frame_I04.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I04, text="I 0.4").grid(padx=10, pady=10)

        frame_I05 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I05.grid(row=0, column=5, sticky="nsew", padx=5, pady=5)
        frame_I05.grid_columnconfigure((0), weight=1)
        frame_I05.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I05, text="I 0.5").grid(padx=10, pady=10)

        frame_I06 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I06.grid(row=0, column=6, sticky="nsew", padx=5, pady=5)
        frame_I06.grid_columnconfigure((0), weight=1)
        frame_I06.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I06, text="I 0.6").grid(padx=10, pady=10)

        frame_I07 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I07.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame_I07.grid_columnconfigure((0), weight=1)
        frame_I07.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I07, text="I 0.7").grid(padx=10, pady=10)

        frame_I10 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I10.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        frame_I10.grid_columnconfigure((0), weight=1)
        frame_I10.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I10, text="I 1.0").grid(padx=10, pady=10)

        frame_I11 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I11.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        frame_I11.grid_columnconfigure((0), weight=1)
        frame_I11.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I11, text="I 1.1").grid(padx=10, pady=10)

        frame_I12 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I12.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)
        frame_I12.grid_columnconfigure((0), weight=1)
        frame_I12.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I12, text="I 1.2").grid(padx=10, pady=10)

        frame_I13 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I13.grid(row=1, column=4, sticky="nsew", padx=5, pady=5)
        frame_I13.grid_columnconfigure((0), weight=1)
        frame_I13.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I13, text="I 1.3").grid(padx=10, pady=10)

        frame_I14 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I14.grid(row=1, column=5, sticky="nsew", padx=5, pady=5)
        frame_I14.grid_columnconfigure((0), weight=1)
        frame_I14.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I14, text="I 1.4").grid(padx=10, pady=10)

        frame_I15 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_I15.grid(row=1, column=6, sticky="nsew", padx=5, pady=5)
        frame_I15.grid_columnconfigure((0), weight=1)
        frame_I15.grid_rowconfigure((0, 1), weight=1)
        Label(frame_I15, text="I 1.5").grid(padx=10, pady=10)
        # LEDs Creation
        LED_I00 = Canvas(frame_I00, width=50, height=50, bg="grey")
        LED_I01 = Canvas(frame_I01, width=50, height=50, bg="grey")
        LED_I02 = Canvas(frame_I02, width=50, height=50, bg="grey")
        LED_I03 = Canvas(frame_I03, width=50, height=50, bg="grey")
        LED_I04 = Canvas(frame_I04, width=50, height=50, bg="grey")
        LED_I05 = Canvas(frame_I05, width=50, height=50, bg="grey")
        LED_I06 = Canvas(frame_I06, width=50, height=50, bg="grey")
        LED_I07 = Canvas(frame_I07, width=50, height=50, bg="grey")
        LED_I10 = Canvas(frame_I10, width=50, height=50, bg="grey")
        LED_I11 = Canvas(frame_I11, width=50, height=50, bg="grey")
        LED_I12 = Canvas(frame_I12, width=50, height=50, bg="grey")
        LED_I13 = Canvas(frame_I13, width=50, height=50, bg="grey")
        LED_I14 = Canvas(frame_I14, width=50, height=50, bg="grey")
        LED_I15 = Canvas(frame_I15, width=50, height=50, bg="grey")

        # LEDs positioning
        LED_I00.grid(row=1, column=0)
        LED_I01.grid(row=1, column=0)
        LED_I02.grid(row=1, column=0)
        LED_I03.grid(row=1, column=0)
        LED_I04.grid(row=1, column=0)
        LED_I05.grid(row=1, column=0)
        LED_I06.grid(row=1, column=0)
        LED_I07.grid(row=1, column=0)
        LED_I10.grid(row=1, column=0)
        LED_I11.grid(row=1, column=0)
        LED_I12.grid(row=1, column=0)
        LED_I13.grid(row=1, column=0)
        LED_I14.grid(row=1, column=0)
        LED_I15.grid(row=1, column=0)

        # Output section tools tab
        lower_title = Label(tab2, text="Outputs")
        lower_title.grid(row=2, column=0, padx=1, pady=1)
        lower_section = ttk.Frame(tab2, borderwidth=2, relief="groove")
        lower_section.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        Label(lower_section, text="outputs").grid(padx=10, pady=10)
        lower_section.grid_rowconfigure((0, 1), weight=1)
        lower_section.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        frame_Q00 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q00.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame_Q00.grid_columnconfigure((0), weight=1)
        frame_Q00.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q00, text="Q 0.0").grid(padx=10, pady=10)

        frame_Q01 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q01.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        frame_Q01.grid_columnconfigure((0), weight=1)
        frame_Q01.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q01, text="Q 0.1").grid(padx=10, pady=10)

        frame_Q02 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q02.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        frame_Q02.grid_columnconfigure((0), weight=1)
        frame_Q02.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q02, text="Q 0.2").grid(padx=10, pady=10)

        frame_Q03 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q03.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        frame_Q03.grid_columnconfigure((0), weight=1)
        frame_Q03.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q03, text="Q 0.3").grid(padx=10, pady=10)

        frame_Q04 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q04.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)
        frame_Q04.grid_columnconfigure((0), weight=1)
        frame_Q04.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q04, text="Q 0.4").grid(padx=10, pady=10)

        frame_Q05 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q05.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame_Q05.grid_columnconfigure((0), weight=1)
        frame_Q05.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q05, text="Q 0.5").grid(padx=10, pady=10)

        frame_Q06 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q06.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        frame_Q06.grid_columnconfigure((0), weight=1)
        frame_Q06.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q06, text="Q 0.6").grid(padx=10, pady=10)

        frame_Q07 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q07.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        frame_Q07.grid_columnconfigure((0), weight=1)
        frame_Q07.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q07, text="Q 0.7").grid(padx=10, pady=10)

        frame_Q10 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q10.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)
        frame_Q10.grid_columnconfigure((0), weight=1)
        frame_Q10.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q10, text="Q 1.0").grid(padx=10, pady=10)

        frame_Q11 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q11.grid(row=1, column=4, sticky="nsew", padx=5, pady=5)
        frame_Q11.grid_columnconfigure((0), weight=1)
        frame_Q11.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q11, text="Q 1.1").grid(padx=10, pady=10)

        # button creation

        button_Q00 = Button(frame_Q00, padx=40, pady=20, bg="grey",
                            command=lambda: [self.handle_button_click("Q00"), print("button O00 is clicked")])
        button_Q01 = Button(frame_Q01, padx=40, pady=20, bg="grey",
                            command=lambda: [self.handle_button_click("Q01"), print("button O01 is clicked")])
        button_Q02 = Button(frame_Q02, padx=40, pady=20, bg="grey",
                            command=lambda: [self.handle_button_click("Q02"), print("button O02 is clicked")])
        button_Q03 = Button(frame_Q03, padx=40, pady=20, bg="grey",
                            command=lambda: [self.handle_button_click("Q03"), print("button O03 is clicked")])
        button_Q04 = Button(frame_Q04, padx=40, pady=20, bg="grey",
                            command=lambda: [self.handle_button_click("Q04"), print("button O04 is clicked")])
        button_Q05 = Button(frame_Q05, padx=40, pady=20, bg="grey",
                            command=lambda: [self.handle_button_click("Q05"), print("button O05 is clicked")])
        button_Q06 = Button(frame_Q06, padx=40, pady=20, bg="grey",
                            command=lambda: [self.handle_button_click("Q06"), print("button O06 is clicked")])
        button_Q07 = Button(frame_Q07, padx=40, pady=20, bg="grey",
                            command=lambda: [self.handle_button_click("Q07"), print("button O07 is clicked")])
        button_Q10 = Button(frame_Q10, padx=40, pady=20, bg="grey",
                            command=lambda: [self.handle_button_click("Q10"), print("button O10 is clicked")])
        button_Q11 = Button(frame_Q11, padx=40, pady=20, bg="grey",
                            command=lambda: [self.handle_button_click("Q11"), print("button O11 is clicked")])

        # button positioning
        button_Q00.grid(row=1, column=0)
        button_Q01.grid(row=1, column=0)
        button_Q02.grid(row=1, column=0)
        button_Q03.grid(row=1, column=0)
        button_Q04.grid(row=1, column=0)
        button_Q05.grid(row=1, column=0)
        button_Q06.grid(row=1, column=0)
        button_Q07.grid(row=1, column=0)
        button_Q10.grid(row=1, column=0)
        button_Q11.grid(row=1, column=0)

        self.widget_addresses = {
            # INPUTS
            "I00": LED_I00,
            "I01": LED_I01,
            "I02": LED_I02,
            "I03": LED_I03,
            "I04": LED_I04,
            "I05": LED_I05,
            "I06": LED_I06,
            "I07": LED_I07,
            "I10": LED_I10,
            "I11": LED_I11,
            "I12": LED_I12,
            "I13": LED_I13,
            "I14": LED_I14,
            "I15": LED_I15,
            # OUTPUTS
            "Q00": button_Q00,
            "Q01": button_Q01,
            "Q02": button_Q02,
            "Q03": button_Q03,
            "Q04": button_Q04,
            "Q05": button_Q05,
            "Q06": button_Q06,
            "Q07": button_Q07,
            "Q10": button_Q10,
            "Q11": button_Q11,

        }

        # sequence edit Tab
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Sequence Edit")
        tab3.grid_rowconfigure((0, 1, 2), weight=1)
        tab3.grid_columnconfigure((0, 1), weight=1)


def main():

    asyncio_thread = AsyncioLoopThread()
    asyncio_thread.start()

    root = Tk()
    app = PLCApp(root, asyncio_thread)
    root.mainloop()


if __name__ == "__main__":
    main()
