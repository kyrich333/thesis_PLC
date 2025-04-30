import asyncio
import threading
from tkinter import Tk, ttk
from plc.my_client import PLCClient


class PLCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PLC_Controller")
        self.root.geometry("800x600")

        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

        self.plc = PLCClient("opc.tcp://192.168.0.1:4840")
        asyncio.run_coroutine_threadsafe(self.plc.connect(), self.loop)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.create_tabs()

    def create_tabs(self):
        # Home Tab
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Home")
        tab1.grid_rowconfigure((0, 1), weight=1)
        tab1.grid_columnconfigure((0), weight=1)

        frame_up = ttk.Frame(tab1, borderwidth=2, relief="groove")
        frame_up.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_up, text="Top Left").pack(padx=10, pady=10)

        frame_lo = ttk.Frame(tab1, borderwidth=2, relief="groove")
        frame_lo.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_lo, text="Top Right").pack(padx=10, pady=10)

        # Tools Tab
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Tools")
        tab2.grid_rowconfigure((0, 1, 2, 3), weight=1)
        tab2.grid_columnconfigure((0), weight=1)

# upper section tools tab
        upper_title = ttk.Label(tab2, text="Inputs")
        upper_title.grid(row=0, column=0, padx=1, pady=1)
        upper_section = ttk.Frame(tab2, borderwidth=2, relief="groove")
        upper_section.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        upper_section.grid_rowconfigure((0, 1), weight=1)
        upper_section.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        frame_00 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_00.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_00, text="I 0.0").grid(padx=10, pady=10)

        frame_01 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_01.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_01, text="I 0.1").grid(padx=10, pady=10)

        frame_02 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_02.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_02, text="I 0.2").grid(padx=10, pady=10)

        frame_03 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_03.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_03, text="I 0.3").grid(padx=10, pady=10)

        frame_04 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_04.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_04, text="I 0.4").grid(padx=10, pady=10)

        frame_05 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_05.grid(row=0, column=5, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_05, text="I 0.5").grid(padx=10, pady=10)

        frame_06 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_06.grid(row=0, column=6, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_06, text="I 0.6").grid(padx=10, pady=10)

        frame_07 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_07.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_07, text="I 0.7").grid(padx=10, pady=10)

        frame_10 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_10.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_10, text="I 1.0").grid(padx=10, pady=10)

        frame_11 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_11.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_11, text="I 1.1").grid(padx=10, pady=10)

        frame_12 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_12.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_12, text="I 1.2").grid(padx=10, pady=10)

        frame_13 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_13.grid(row=1, column=4, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_13, text="I 1.3").grid(padx=10, pady=10)

        frame_14 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_14.grid(row=1, column=5, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_14, text="I 1.4").grid(padx=10, pady=10)

        frame_15 = ttk.Frame(upper_section, borderwidth=2, relief="groove")
        frame_15.grid(row=1, column=6, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_15, text="I 1.5").grid(padx=10, pady=10)

# lower section tools tab
        lower_title = ttk.Label(tab2, text="Outputs")
        lower_title.grid(row=2, column=0, padx=1, pady=1)
        lower_section = ttk.Frame(tab2, borderwidth=2, relief="groove")
        lower_section.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(lower_section, text="outputs").grid(padx=10, pady=10)
        lower_section.grid_rowconfigure((0, 1), weight=1)
        lower_section.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        frame_16 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_16.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_16, text="O 0.0").grid(padx=10, pady=10)

        frame_17 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_17.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_17, text="O 0.1").grid(padx=10, pady=10)

        frame_20 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_20.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_20, text="O 0.2").grid(padx=10, pady=10)

        frame_21 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_21.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_21, text="O 0.3").grid(padx=10, pady=10)

        frame_22 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_22.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_22, text="O 0.4").grid(padx=10, pady=10)

        frame_23 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_23.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_23, text="O 0.5").grid(padx=10, pady=10)

        frame_24 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_24.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_24, text="O 0.6").grid(padx=10, pady=10)

        frame_25 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_25.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_25, text="O 0.7").grid(padx=10, pady=10)

        frame_26 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_26.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_26, text="O 1.0").grid(padx=10, pady=10)

        frame_27 = ttk.Frame(lower_section, borderwidth=2, relief="groove")
        frame_27.grid(row=1, column=4, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_27, text="O 1.1").grid(padx=10, pady=10)

 # sequence edit Tab
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Sequence Edit")
        tab3.grid_rowconfigure((0, 1, 2), weight=1)
        tab3.grid_columnconfigure((0, 1), weight=1)


def main():
    root = Tk()
    app = PLCApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
