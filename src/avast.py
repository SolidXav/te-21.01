class Avast:

    @staticmethod
    def check_anomaly_for_reading(reading, device_list):
        if (reading.kwh is None or
                reading.kwh < 0.0 or
                reading.device_id is None or
                reading.device_id not in device_list or
                reading.avg_power_w is None or
                reading.avg_power_w < 0.0 or
                reading.date_time is None):
            return False
        return True

    @staticmethod
    def check_anomaly_for_device(device):
        if (device.name is None or
                device.device_id is None or
                device.room is None or
                device.rated_power_w is None or
                device.rated_power_w <= 0):
            return False
        return True

    @staticmethod
    def check_anomaly_for_event(event, device_list):
        if (event.device_id is None or
            event.device_id not in device_list):
            return False
        return True

    @staticmethod
    def check_event_pair(start_event, end_event):
        if (start_event.event != "start" or
                end_event.event != "stop" or
                start_event.device_id != end_event.device_id):
            return False
        return True
    ## Avast sprawdza czy event nie idzie w nieskończoność
    @staticmethod
    def scan_for_cost(value):
        if (value is None or
                value < 0.0):
            return False
        return True

    @staticmethod
    def correct_day(reading):
        date = reading.date_time
        if (date and isinstance(date, str) and
                len(date) >= 10):
            return date[:10]
        return None

    @staticmethod
    def check_anomaly_for_efficiency(reading, device_map):
        device_id = reading.device_id
        avg_power_w = reading.avg_power_w
        rated_power_w = reading.rated_power_w
        device = device_map[device_id]
        if (device_id is None or
                device_id not in device_map or
                avg_power_w is None or
                avg_power_w < 0 or
                rated_power_w is None or
                rated_power_w <= 0):
            return False
        return True