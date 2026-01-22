from avast import *

class EfficiencyChecker:
    limit = 100

    @staticmethod
    def calculate_efficiency(rated_power_w, avg_power_w):
        return avg_power_w / rated_power_w * 100

    @classmethod
    def status_of_device(cls, efficiency):
        if efficiency > cls.limit:
            return "Uszkodzone"
        return "Zdrowe"

    def get_avg_with_obj(self, readings, devices):
        devices_data = {}
        for device in devices:
            if Avast.check_anomaly_for_device(device):
                devices_data[device.device_id] = {"obiekt": device, "avg": []}

        for reading in readings:
            if Avast.check_anomaly_for_efficiency(reading, {devid: device["obiekt"] for devid, device in devices_data.items()}):
                devid = reading.device_id
                if devid in devices_data:
                    devices_data[devid]["avg"].append(reading.avg_power_w)
        return devices_data

    def map_status_to_obj(self, mapa):
        devices_data = {device: [] for device in mapa}
        for device_id, device in mapa.items():
            for avg in device["avg"]:
                devices_data[device_id] += [self.status_of_device(self.calculate_efficiency(device["obiekt"].rated_power_w, avg))]
        result = {}
        for device_id, device in devices_data.items():
            if "Uszkodzone" in device:
                result[device_id] = "Uszkodzone"
        return result
