import asyncio
import threading
from tkinter import Tk, ttk, Button, Label
from plc.my_client import PLCClient
from asyncua import ua
from asyncio import run_coroutine_threadsafe
# opcua/nodes.py


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
        self.asyncio_thread = asyncio_thread
        self.root.title("PLC_Controller")
        self.root.geometry("1920x1080")
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

        self.plc = PLCClient("opc.tcp://192.168.0.1:4840")
        asyncio.run_coroutine_threadsafe(self.plc.connect(), self.loop)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)
        self.node_addresses = {
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

            # MEMORY
        }

        self.create_tabs()

    def send_to_client(self, node_id):
        node_address = self.node_addresses.get(node_id)
        if node_address:
            asyncio.run_coroutine_threadsafe(
                self.plc.toggle_output(node_address), self.loop)
            print(f"Sent command to PLC: {node_address}")
        else:
            print(f"Node ID {node_id} not found in node addresses.")

    def create_tabs(self):
        # Home Tab
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Home")
        tab1.grid_rowconfigure((0, 1), weight=1)
        tab1.grid_columnconfigure((0), weight=1)

        frame_up = ttk.Frame(tab1, borderwidth=2, relief="groove")
        frame_up.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        Label(frame_up, text="Top Left").pack(padx=10, pady=10)

        frame_lo = ttk.Frame(tab1, borderwidth=2, relief="groove")
        frame_lo.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        Label(frame_lo, text="Top Right").pack(padx=10, pady=10)

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

        frame_00 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_00.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        Label(frame_00, text="I 0.0").grid(padx=10, pady=10)

        frame_01 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_01.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        Label(frame_01, text="I 0.1").grid(padx=10, pady=10)

        frame_02 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_02.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        Label(frame_02, text="I 0.2").grid(padx=10, pady=10)

        frame_03 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_03.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        Label(frame_03, text="I 0.3").grid(padx=10, pady=10)

        frame_04 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_04.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)
        Label(frame_04, text="I 0.4").grid(padx=10, pady=10)

        frame_05 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_05.grid(row=0, column=5, sticky="nsew", padx=5, pady=5)
        Label(frame_05, text="I 0.5").grid(padx=10, pady=10)

        frame_06 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_06.grid(row=0, column=6, sticky="nsew", padx=5, pady=5)
        Label(frame_06, text="I 0.6").grid(padx=10, pady=10)

        frame_07 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_07.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        Label(frame_07, text="I 0.7").grid(padx=10, pady=10)

        frame_10 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_10.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        Label(frame_10, text="I 1.0").grid(padx=10, pady=10)

        frame_11 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_11.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        Label(frame_11, text="I 1.1").grid(padx=10, pady=10)

        frame_12 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_12.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)
        Label(frame_12, text="I 1.2").grid(padx=10, pady=10)

        frame_13 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_13.grid(row=1, column=4, sticky="nsew", padx=5, pady=5)
        Label(frame_13, text="I 1.3").grid(padx=10, pady=10)

        frame_14 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_14.grid(row=1, column=5, sticky="nsew", padx=5, pady=5)
        Label(frame_14, text="I 1.4").grid(padx=10, pady=10)

        frame_15 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_15.grid(row=1, column=6, sticky="nsew", padx=5, pady=5)
        Label(frame_15, text="I 1.5").grid(padx=10, pady=10)

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
        Label(frame_Q00, text="O 0.0").grid(padx=10, pady=10)

        frame_Q01 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q01.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        frame_Q01.grid_columnconfigure((0), weight=1)
        frame_Q01.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q01, text="O 0.1").grid(padx=10, pady=10)

        frame_Q02 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q02.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        frame_Q02.grid_columnconfigure((0), weight=1)
        frame_Q02.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q02, text="O 0.2").grid(padx=10, pady=10)

        frame_Q03 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q03.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        frame_Q03.grid_columnconfigure((0), weight=1)
        frame_Q03.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q03, text="O 0.3").grid(padx=10, pady=10)

        frame_Q04 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q04.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)
        frame_Q04.grid_columnconfigure((0), weight=1)
        frame_Q04.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q04, text="O 0.4").grid(padx=10, pady=10)

        frame_Q05 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q05.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame_Q05.grid_columnconfigure((0), weight=1)
        frame_Q05.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q05, text="O 0.5").grid(padx=10, pady=10)

        frame_Q06 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q06.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        frame_Q06.grid_columnconfigure((0), weight=1)
        frame_Q06.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q06, text="O 0.6").grid(padx=10, pady=10)

        frame_Q07 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q07.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        frame_Q07.grid_columnconfigure((0), weight=1)
        frame_Q07.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q07, text="O 0.7").grid(padx=10, pady=10)

        frame_Q10 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q10.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)
        frame_Q10.grid_columnconfigure((0), weight=1)
        frame_Q10.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q10, text="O 1.0").grid(padx=10, pady=10)

        frame_Q11 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_Q11.grid(row=1, column=4, sticky="nsew", padx=5, pady=5)
        frame_Q11.grid_columnconfigure((0), weight=1)
        frame_Q11.grid_rowconfigure((0, 1), weight=1)
        Label(frame_Q11, text="O 1.1").grid(padx=10, pady=10)

        # button creation

        button_Q00 = Button(frame_Q00, padx=40, pady=20,
                            command=lambda: [self.send_to_client("Q00"), print("button O00 is clicked")])
        button_Q01 = Button(frame_Q01, padx=40, pady=20,
                            command=lambda: [self.send_to_client("ns=4;i=5"), print("button O01 is clicked")])
        button_Q02 = Button(frame_Q02, padx=40, pady=20,
                            command=lambda: print("button O02 is clicked"))
        button_Q03 = Button(frame_Q03, padx=40, pady=20,
                            command=lambda: print("button O03 is clicked"))
        button_Q04 = Button(frame_Q04, padx=40, pady=20,
                            command=lambda: print("button O04 is clicked"))
        button_Q05 = Button(frame_Q05, padx=40, pady=20,
                            command=lambda: print("button O05 is clicked"))
        button_Q06 = Button(frame_Q06, padx=40, pady=20,
                            command=lambda: print("button O06 is clicked"))
        button_Q07 = Button(frame_Q07, padx=40, pady=20,
                            command=lambda: print("button O07 is clicked"))
        button_Q10 = Button(frame_Q10, padx=40, pady=20,
                            command=lambda: print("button O10 is clicked"))
        button_Q11 = Button(frame_Q11, padx=40, pady=20,
                            command=lambda: print("button O11 is clicked"))

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
