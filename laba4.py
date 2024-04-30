import tkinter as tk
from tkinter import Label, Entry, Button, OptionMenu, Frame, Listbox
from PIL import Image, ImageTk

from classes import Thermometer


class Application(tk.Tk):
    def __init__(self, device):
        super().__init__()
        self.device = device
        self.current_image_index = 0
        self.images = [
            ImageTk.PhotoImage(Image.open("./images/air-thermometer.jpg")),
            ImageTk.PhotoImage(Image.open("./images/body-thermometer.jpg")),
            ImageTk.PhotoImage(Image.open("./images/electro-thermometer.jpg"))
        ]

        self.title("Temperature Device")
        self.create_widgets()

    def create_widgets(self):
        # Header
        self.info_label = Label(
            self, text=self.device.display_info(), padx=10, pady=10)
        self.info_label.pack()

        self.temperature_label = Label(self, text="Temperature:")
        self.temperature_label.pack()
        self.temperature_entry = Entry(self)
        self.temperature_entry.pack()

        self.model_label = Label(self, text="Model:")
        self.model_label.pack()
        self.model_entry = Entry(self)
        self.model_entry.pack()

        self.brand_label = Label(self, text="Brand:")
        self.brand_label.pack()
        self.brand_entry = Entry(self)
        self.brand_entry.pack()

        self.units_label = Label(self, text="Units:")
        self.units_label.pack()
        self.units_var = tk.StringVar(self)
        self.units_var.set("Celsius")
        self.units_options = OptionMenu(
            self, self.units_var, "Celsius", "Fahrenheit", "Kelvin")
        self.units_options.pack()

        self.show_values_button = Button(
            self, text="Show Values", command=self.display_values)
        self.show_values_button.pack()

        # work with history_listbox
        self.history_frame = Frame(self)
        self.history_frame.pack()

        # btns list
        history_button_texts = ["Add Temperature", "Edit Temperature", "Sort Temperatures",
                                "Remove Temperature", "Reverse Temperatures", "Check if Empty", "Check Size"]
        self.history_buttons = []
        for button_text in history_button_texts:
            button = Button(self.history_frame, text=button_text,
                            command=lambda op=button_text: self.execute_history_operation(op))
            button.pack(side=tk.TOP, fill=tk.X)
            self.history_buttons.append(button)

        self.history_input_frame = Frame(self)
        self.history_input_frame.pack()

        self.status_label = Label(self, text="")
        self.status_label.pack()

        self.history_input_label = Label(
            self.history_input_frame, text="Enter temperature:")
        self.history_input_label.pack(side=tk.LEFT)
        self.history_input_entry = Entry(self.history_input_frame)
        self.history_input_entry.pack(side=tk.LEFT)

        self.history_listbox = Listbox(self, width=50)
        self.history_listbox.pack()

        # work with img
        self.prev_button = Button(
            self, text="<< Previous", command=self.show_previous_image)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = Button(
            self, text="Next >>", command=self.show_next_image)
        self.next_button.pack(side=tk.RIGHT)

        self.image_label = Label(
            self, image=self.images[self.current_image_index])
        self.image_label.pack()

    def show_next_image(self):
        self.current_image_index = (
            self.current_image_index + 1) % len(self.images)
        self.image_label.config(image=self.images[self.current_image_index])

    def show_previous_image(self):
        self.current_image_index = (
            self.current_image_index - 1) % len(self.images)
        self.image_label.config(image=self.images[self.current_image_index])

    def display_values(self):
        temperature = round(float(self.temperature_entry.get()), 2)
        model = self.model_entry.get()
        brand = self.brand_entry.get()
        units = self.units_var.get()

        if units != self.device.units:
            self.device.change_units(units)
            temperature = self.device.temperature

        self.device.temperature = temperature
        self.device.model = model
        self.device.brand = brand
        self.device.units = units
        self.info_label.config(text=self.device.display_info())
        self.update_history_listbox()

    def execute_history_operation(self, operation):
        if operation == "Add Temperature":
            temperature = round(float(self.history_input_entry.get()), 2)
            self.device.add_temperature_to_history(temperature)
        elif operation == "Edit Temperature":
            selected_temperature = self.history_listbox.get(
                self.history_listbox.curselection())
            if selected_temperature:
                new_temperature = round(
                    float(self.history_input_entry.get()), 2)
                self.device.edit_temperature_in_history(self.device.temperature_history.index(
                    float(selected_temperature)), new_temperature)
        elif operation == "Sort Temperatures":
            self.device.sort_temperature_history()
        elif operation == "Remove Temperature":
            temperature = round(float(self.history_input_entry.get()), 2)
            self.device.remove_temperature_from_history(temperature)
        elif operation == "Reverse Temperatures":
            self.device.reverse_temperature_history()
        elif operation == "Check if Empty":
            if self.device.is_temperature_history_empty():
                self.status_label.config(text="Temperature history is empty.")
            else:
                self.status_label.config(
                    text="Temperature history is not empty.")
        elif operation == "Check Size":
            self.status_label.config(
                text=f"Temperature history size: {self.device.check_temperature_history_size()}")
        self.update_history_listbox()

    def update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for temperature in self.device.temperature_history:
            self.history_listbox.insert(tk.END, str(temperature))


# Створення об'єкта класу Thermometer
thermometer = Thermometer("Digital Thermometer")

# Створення та запуск графічного інтерфейсу
app = Application(thermometer)
app.mainloop()
