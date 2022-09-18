import time
from gatewayn.sensor.sensor import Sensor

class BatterySensor(Sensor):
    
    def __init__(self):
        super(BatterySensor, self).__init__()
        self.name: str = "BatterySensor"
        self.measurements: list[BatterySensor.BatteryMeasurement] = []

    def read_data_from_advertisement(self, data: dict[str, any]):
        measurement = BatterySensor.BatteryMeasurement(voltage=data.get("battery", 0) / 1000, sequence_number=data.get("sequence_number", 0), data_format=data.get("data_format", 0))
        self.measurements.append(measurement)
        self.logger.debug(f"read voltage: {measurement}")
        return

    class BatteryMeasurement:
        def __init__(self, voltage: float = 0.0, sequence_number: int = 0, data_format: int = 0) -> None:
            self.voltage = voltage
            self.sequence_number: int = sequence_number
            self.data_format: int = data_format
            self.recorded_time: float = time.time()


        def get_props(self):
            return self.__dict__
