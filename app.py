import tkinter as tk
from tkinter import ttk, messagebox
import sys

from converter import UnitConverter
from constants import UNIT_GROUPS


class UnitConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер единиц физических величин")
        self.root.geometry("500x300")
        self.root.resizable(True, True)

        self.current_group = "Температура"
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выход", command=self.exit_app)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

    def create_widgets(self):
        tk.Label(self.root, text="Группа величин:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.group_combo = ttk.Combobox(self.root, values=list(UNIT_GROUPS.keys()), state="readonly")
        self.group_combo.set(self.current_group)
        self.group_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.group_combo.bind("<<ComboboxSelected>>", self.on_group_change)

        tk.Label(self.root, text="Из:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.from_unit_combo = ttk.Combobox(self.root, state="readonly")
        self.from_unit_combo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.from_unit_combo.bind("<<ComboboxSelected>>", self.update_to_units)

        tk.Label(self.root, text="Значение:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.from_entry = tk.Entry(self.root)
        self.from_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self.root, text="В:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.to_unit_combo = ttk.Combobox(self.root, state="readonly")
        self.to_unit_combo.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self.root, text="Результат:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.to_entry = tk.Entry(self.root, state="readonly")
        self.to_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        convert_button = tk.Button(self.root, text="Конвертировать", command=self.convert)
        convert_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.root.grid_columnconfigure(1, weight=1)
        self.update_from_units()

    def on_group_change(self, event=None):
        self.current_group = self.group_combo.get()
        self.update_from_units()

    def update_from_units(self):
        units = UNIT_GROUPS[self.current_group]
        self.from_unit_combo['values'] = units
        if units:
            self.from_unit_combo.set(units[0])
            self.update_to_units()

    def update_to_units(self, event=None):
        from_unit = self.from_unit_combo.get()
        units = UNIT_GROUPS[self.current_group]
        to_units = [u for u in units if u != from_unit]
        self.to_unit_combo['values'] = to_units
        if to_units:
            self.to_unit_combo.set(to_units[0])

    def convert(self):
        try:
            from_unit = self.from_unit_combo.get()
            to_unit = self.to_unit_combo.get()
            value_str = self.from_entry.get().strip()

            if not value_str:
                raise ValueError("Введите значение для конвертации.")

            value = float(value_str)
            result = UnitConverter.convert(value, from_unit, to_unit)

            self.to_entry.config(state="normal")
            self.to_entry.delete(0, tk.END)
            self.to_entry.insert(0, f"{result:.6f}")
            self.to_entry.config(state="readonly")

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Неизвестная ошибка", f"Произошла ошибка: {e}")

    def show_about(self):
        about_text = (
            "Конвертер единиц физических величин\n"
        )
        messagebox.showinfo("О программе", about_text)

    def exit_app(self):
        self.root.quit()
        self.root.destroy()
        sys.exit(0)