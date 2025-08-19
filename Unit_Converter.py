import tkinter as tk
from tkinter import font, ttk
from unit_convert import UnitConvert as converter
import re

root = tk.Tk()
root.geometry("500x450")
root.title("Unit Converter")
root.iconbitmap(r'icon.ico')
root.configure(bg="#222E36")


radio_var = tk.StringVar(value="Weight")

units = {
    "Weight": ["Kilogram (kg)", "Gram (g)", "Milligram (mg)", "Pound (lb)", "Ounce (oz)"],
    "Length": ["Meter (m)", "Centimeter (cm)", "Millimeter (mm)", "Kilometer (km)", "Mile (mi)", "Yard (yd)", "Foot (ft)", "Inch (in)"],
    "Temperature": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]
}

title_lbl = tk.Label(root, text= "Unit Converter", font = ("Arial", 26), bg="#222E36", fg="white")
title_lbl.pack(pady=(30,0))

error_label = ""
error_lbl = tk.Label(root, textvariable = error_label, font = ("Arial", 20), bg="#222E36", fg="red")
error_lbl.pack(pady=(50,0))

radio_frame = tk.Frame(root, bg="#222E36")
radio_frame.pack(pady=(20,5))

custom_font = font.Font(size=14)

radio_style = {
    "font": custom_font,
    "bg": "#222E36",
    "fg": "white",
    "selectcolor": "#222E36",
    "activebackground": "#222E36",
    "activeforeground": "white",
    "cursor": "hand2",
    "indicatoron": 1,
    "padx": 5,
    "pady": 5
}

for text in ["Weight", "Length", "Temperature"]:
    tk.Radiobutton(radio_frame, variable=radio_var, value=text, text=text, **radio_style,
                   command=lambda: update_units()).pack(side="left", padx=10)


unit_frame = tk.Frame(root, bg="#222E36")
unit_frame.pack(pady=(0, 0))

left_unit_var = tk.StringVar()
right_unit_var = tk.StringVar()

left_dropdown = ttk.Combobox(unit_frame, textvariable=left_unit_var, state="readonly", font=("Arial", 12))
arrow_lbl=  tk.Label(unit_frame, text="=>", font=("Arial", 16), bg="#222E36", fg="white")
right_dropdown = ttk.Combobox(unit_frame, textvariable=right_unit_var, state="readonly", font=("Arial", 12))

left_dropdown.grid(row=0, column=0, padx=10)
arrow_lbl.grid(row=0, column=1, padx=10)
right_dropdown.grid(row=0, column=2, padx=10)

# Frame for entry boxes
entry_frame = tk.Frame(root, bg="#222E36")
entry_frame.pack(pady=20)

left_entry_var = tk.StringVar()
right_entry_var = tk.StringVar(value="")

left_entry = tk.Entry(entry_frame, textvariable=left_entry_var, font=("Arial", 14), width=15)
arrow_lbl=  tk.Label(entry_frame, text="=>", font=("Arial", 16), bg="#222E36", fg="white")
right_entry = tk.Entry(entry_frame, textvariable=right_entry_var, font=("Arial", 14), width=15, state="readonly")

left_entry.grid(row=0, column=0, padx=10)
arrow_lbl.grid(row=0, column=1, padx=10)
right_entry.grid(row=0, column=2, padx=10)

def update_units():
    category = radio_var.get()
    left_dropdown["values"] = units[category]
    right_dropdown["values"] = units[category]
    left_unit_var.set(units[category][0])
    right_unit_var.set(units[category][1] if len(units[category]) > 1 else units[category][0])

def extract_unit(unit_text: str) -> str:
    if "(" in unit_text and ")" in unit_text:
        return unit_text.split("(")[-1].replace(")", "").strip()
    return unit_text.strip()

UNIT_MAP = {
    "kg": "kg",
    "g": "g",
    "mg": "mg",
    "lb": "lbs",
    "oz": "oz",
    "m": "m",
    "cm": "cm",
    "mm": "mm",
    "km": "km",
    "mi": "mi",
    "yd": "yd",
    "ft": "ft",
    "in": "i",
    "°C": "c",
    "°F": "f",
    "K": "k"
}

def convert():
    error_lbl.config(text="")
    right_entry_var.set("")

    from_unit = extract_unit(left_unit_var.get())
    to_unit = extract_unit(right_unit_var.get())

    from_unit_mapped = UNIT_MAP.get(from_unit, from_unit)
    to_unit_mapped = UNIT_MAP.get(to_unit, to_unit)

    try:
        num_to_convert = float(left_entry_var.get())
    except ValueError:
        error_lbl.config(text="Invalid Input")
    else:
        try:
            converted_num = converter(from_unit_mapped, num_to_convert)[to_unit_mapped]
            right_entry_var.set(converted_num)
        except Exception as e:
            error_lbl.config(text=f"Conversion not supported: {e}", font=("Arial", 16))



convert_btn = tk.Button(root, text="Convert", font=("Arial", 18), bg="#4CAF50", fg="white",relief="flat", cursor="hand2", command=convert)
convert_btn.pack(pady=20, padx=10)

update_units()

root.mainloop()
