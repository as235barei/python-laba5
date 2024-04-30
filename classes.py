class TemperatureDevice:
    def __init__(self, name, temperature=0, model="", brand="", units="Celsius"):
        self.name = name
        self.temperature = temperature
        self.model = model
        self.brand = brand
        self.units = units
        self.temperature_history = []

    def display_info(self):
        return f"Device: {self.name}\nTemperature: {self.temperature} {self.units}\nModel: {self.model}\nBrand: {self.brand}"

    def add_temperature_to_history(self, temperature):
        self.temperature_history.append(temperature)

    def edit_temperature_in_history(self, index, new_temperature):
        if 0 <= index < len(self.temperature_history):
            self.temperature_history[index] = new_temperature
        else:
            print("Index out of range.")

    def sort_temperature_history(self):
        self.temperature_history.sort()

    def remove_temperature_from_history(self, temperature):
        if temperature in self.temperature_history:
            self.temperature_history.remove(temperature)
        else:
            print("Temperature not found in history.")

    def is_temperature_history_empty(self):
        return len(self.temperature_history) == 0

    def reverse_temperature_history(self):
        self.temperature_history.reverse()

    def check_temperature_history_size(self):
        return len(self.temperature_history)

    def change_units(self, new_units):
        if self.units == "Celsius" and new_units == "Fahrenheit":
            self.temperature = self.temperature * 9/5 + 32
        elif self.units == "Celsius" and new_units == "Kelvin":
            self.temperature = self.temperature + 273.15
        elif self.units == "Fahrenheit" and new_units == "Celsius":
            self.temperature = (self.temperature - 32) * 5/9
        elif self.units == "Fahrenheit" and new_units == "Kelvin":
            self.temperature = (self.temperature + 459.67) * 5/9
        elif self.units == "Kelvin" and new_units == "Celsius":
            self.temperature = self.temperature - 273.15
        elif self.units == "Kelvin" and new_units == "Fahrenheit":
            self.temperature = self.temperature * 9/5 - 459.67
        self.units = new_units


class Thermometer(TemperatureDevice):
    def __init__(self, name, temperature=0, model="", brand="", units="Celsius"):
        super().__init__(name, temperature, model, brand, units)

    def display_info(self):
        return f"Device: {self.name}\n\nTemperature: {self.temperature}° {self.units}\nModel: {self.model}\nBrand: {self.brand}"
