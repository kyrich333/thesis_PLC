import tkinter as tk
from tkinter import ttk


class PLCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PLC_Controller")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.create_tabs()

    def create_tabs(self):
        # Home Tab
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Home")
        tab1.grid_rowconfigure((0, 1), weight=1)
        tab1.grid_columnconfigure((0, 1), weight=1)

        frame_tl = ttk.Frame(tab1, borderwidth=2, relief="groove")
        frame_tl.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_tl, text="Top Left").pack(padx=10, pady=10)

        frame_tr = ttk.Frame(tab1, borderwidth=2, relief="groove")
        frame_tr.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_tr, text="Top Right").pack(padx=10, pady=10)

        frame_bl = ttk.Frame(tab1, borderwidth=2, relief="groove")
        frame_bl.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_bl, text="Bottom Left").pack(padx=10, pady=10)

        frame_br = ttk.Frame(tab1, borderwidth=2, relief="groove")
        frame_br.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_br, text="Bottom Right").pack(padx=10, pady=10)

        # Tools Tab
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Tools")
        tab2.grid_rowconfigure((0, 1, 2), weight=1)
        tab2.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        frame_00 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_00.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_00, text="Tool 1").pack(padx=10, pady=10)

        frame_01 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_01.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_01, text="Tool 2").pack(padx=10, pady=10)

        frame_02 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_02.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_02, text="Tool 3").pack(padx=10, pady=10)

        frame_03 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_03.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_03, text="Tool 4").pack(padx=10, pady=10)

        frame_04 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_04.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_04, text="Tool 5").pack(padx=10, pady=10)

        frame_05 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_05.grid(row=0, column=5, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_05, text="Tool 6").pack(padx=10, pady=10)

        frame_06 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_06.grid(row=0, column=6, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_06, text="Tool 7").pack(padx=10, pady=10)

        frame_07 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_07.grid(row=0, column=7, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_07, text="Tool 8").pack(padx=10, pady=10)

        frame_10 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_10.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_10, text="Tool 9").pack(padx=10, pady=10)

        frame_11 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_11.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_11, text="Tool 10").pack(padx=10, pady=10)

        frame_12 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_12.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_12, text="Tool 11").pack(padx=10, pady=10)

        frame_13 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_13.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_13, text="Tool 12").pack(padx=10, pady=10)

        frame_14 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_14.grid(row=1, column=4, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_14, text="Tool 13").pack(padx=10, pady=10)

        frame_15 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_15.grid(row=1, column=5, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_15, text="Tool 14").pack(padx=10, pady=10)

        frame_16 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_16.grid(row=1, column=6, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_16, text="Tool 15").pack(padx=10, pady=10)

        frame_17 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_17.grid(row=1, column=7, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_17, text="Tool 16").pack(padx=10, pady=10)

        frame_20 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_20.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_20, text="Tool 17").pack(padx=10, pady=10)

        frame_21 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_21.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_21, text="Tool 18").pack(padx=10, pady=10)

        frame_22 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_22.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_22, text="Tool 19").pack(padx=10, pady=10)

        frame_23 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_23.grid(row=2, column=3, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_23, text="Tool 20").pack(padx=10, pady=10)

        frame_24 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_24.grid(row=2, column=4, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_24, text="Tool 21").pack(padx=10, pady=10)

        frame_25 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_25.grid(row=2, column=5, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_25, text="Tool 22").pack(padx=10, pady=10)

        frame_26 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_26.grid(row=2, column=6, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_26, text="Tool 23").pack(padx=10, pady=10)

        frame_27 = ttk.Frame(tab2, borderwidth=2, relief="groove")
        frame_27.grid(row=2, column=7, sticky="nsew", padx=5, pady=5)
        ttk.Label(frame_27, text="Tool 24").pack(padx=10, pady=10)


def main():
    root = tk.Tk()
    app = PLCApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
