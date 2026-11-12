class TemperatureDisplay:
    def __init__(self):
        self.displayedCelsius = None

    def refresh(self):
        pass

class TemperatureSensor:
    def __init__(self):
        self.currentCelsius = None

    def readCelsius(self):
        pass


def run_sequence():
    display = TemperatureDisplay()
    sensor = TemperatureSensor()

    sensor.readCelsius()
