import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import json
import random


def main():
    def convert_data(source_data, output_file_name):
        preamp_gain = 0.0

        converted_data = {
            "name": output_file_name,
            "preamp": {preamp_gain},
            "parametric": True,
            "bands": [],
        }
        for i in range(2):
            band = {
                "type": i,
                "channels": 0,
                "frequency": (90 if i == 0 else 10000),
                "q": 0.7,
                "gain": 0.0,
                "color": 0,
            }
            converted_data["bands"].append(band)

        for line in source_data:
            if line.strip():
                if line.startswith("Filter"):
                    parts = line.split()
                    filter_type = parts[3]
                    freq = int(float(parts[5]))
                    gain = float(parts[8])
                    q = float(parts[11])
                    band = {
                        "type": (
                            0
                            if filter_type == "LSC"
                            else 1 if filter_type == "HSC" else 3
                        ),
                        "channels": 0,
                        "frequency": freq,
                        "q": q,
                        "gain": gain,
                        "color": (random.randint(-15628237, 15628237)),
                    }
                    converted_data["bands"].append(band)
                elif line.startswith("Preamp"):
                    parts = line.split()
                    preamp_gain = float(parts[1])
                    converted_data["preamp"] = preamp_gain

        return converted_data

    def on_drop(event):
        file_path = event.data
        file_path = file_path[1:-1]
        if file_path:
            output_file_name = output_file_name_entry.get()
            if output_file_name == "":
                output_file_name = "default_file_name"
            try:
                with open(file_path, "r") as file:
                    source_data = file.readlines()
                    converted_data = convert_data(source_data, output_file_name)
                    output_file_path = filedialog.asksaveasfilename(
                        defaultextension=".json", 
                        filetypes=[("JSON files", "*.json")],
                        initialfile=output_file_name  # Ustawienie początkowej nazwy pliku
                    )
                    with open(output_file_path, "w") as output_file:
                        json.dump(converted_data, output_file, indent="\t")
                    status_label.config(text="Plik JSON został zapisany.")

                with open(output_file_path, "r+") as output_file:
                    source_data = output_file.read()
                    source_data = "[" + source_data + "\n]"
                    output_file.seek(0)
                    output_file.write(source_data)
                    output_file.truncate()
            except FileNotFoundError:
                status_label.config(text="Plik nie został znaleziony.")

    root = TkinterDnD.Tk()
    root.title("Konwerter danych audio")

    frame = tk.Frame(root, width=800, height=400)
    frame.grid(row=0, column=0, padx=10, pady=10)

    tk.Label(frame, text="Nazwa pliku wyjściowego:").grid(row=0, column=0, sticky="w")
    output_file_name_entry = tk.Entry(frame)
    output_file_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(frame, text="Przeciągnij plik txt:").grid(row=1, column=0, sticky="w")

    status_label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_label.grid(row=1, column=0, sticky="ew")

    frame.drop_target_register(DND_FILES)
    frame.dnd_bind("<<Drop>>", on_drop)
    root.mainloop()


main()
