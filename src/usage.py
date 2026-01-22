from avast import *

class DeviceMapper:

    def __init__(self, readings, device_to_room):
        self.readings = readings
        self.device_to_room = device_to_room

    def map(self):
        devices = set(self.device_to_room.keys())
        usage = {}
        for reading in self.readings:
            if Avast.check_anomaly_for_reading(reading, devices):
                deviceid = reading.device_id
                usage[deviceid] = round(usage.get(deviceid, 0) + reading.kwh,4)
        return usage

class RoomMapper:

    def __init__(self, device_to_room, all_rooms):
        self.device_to_room = device_to_room
        self.all_rooms = all_rooms

    def map(self, usage_per_device):
        usage = {room: 0.0 for room in self.all_rooms}
        for device_id, kwh in usage_per_device.items():
            room = self.device_to_room.get(device_id, "Unknown")
            if room:
                usage[room] = round(usage.get(room, 0.0) + kwh,4)
        return usage

class PersonMapper:

    def __init__(self, room_to_person, everyone_ids):
        self.room_to_person = room_to_person
        self.all_everyone_ids = everyone_ids

    def map(self, usage_per_room):
        usage = {person_id: 0.0 for person_id in self.all_everyone_ids}
        usage["Everyone"] = 0.0
        for room, kwh in usage_per_room.items():
            person = self.room_to_person.get(room, "Everyone")
            if person in usage:
                usage[person] += round(kwh,4)
            else:
                usage["Everyone"] += round(kwh,4)
        return usage

class DayMapper:

    def __init__(self, readings, device_to_room):
        self.readings = readings
        self.device_to_room = device_to_room

    def map(self):
        devices = set(self.device_to_room.keys())
        dates = {}
        for reading in self.readings:
            if Avast.check_anomaly_for_reading(reading, devices):
                day = Avast.correct_day(reading)
                if day:
                    dates[day] = round(dates.get(day, 0) + reading.kwh,4)
        return dates

class Usage:
    def __init__(self, readings, device_list, household_list):
        self.readings = readings
        self.household_list = household_list
        household_rooms = {person.room for person in household_list if person.room is not None}
        devices_rooms = {device.room for device in device_list if device.room is not None}
        self.device_map = {device.device_id: device for device in device_list}
        self.all_rooms = household_rooms | devices_rooms
        self.room_to_person = {person.room: person.person_id for person in household_list if person.room is not None}
        self.device_to_room = {device.device_id: device.room for device in device_list if device.room is not None}
        self.everyone_ids = {person.person_id for person in household_list}
        ## Unia daje nam wszystkie pokoje bez powtórzeń
        ## Tworzymy dwa osobne sety, ponieważ nie wszystkie pokoje zawierają się w klasie Household i nie każde urządzenie ma swojego właściciela

    def get_usage_per_device(self):
        mapper = DeviceMapper(self.readings, self.device_map)
        return mapper.map()

    def get_usage_per_room(self):
        usage_per_device = self.get_usage_per_device()
        mapper = RoomMapper(self.device_to_room, self.all_rooms)
        return mapper.map(usage_per_device)

    def get_usage_per_household(self):
        usage_per_room = self.get_usage_per_room()
        mapper = PersonMapper(self.room_to_person, self.everyone_ids)
        return mapper.map(usage_per_room)

    def get_usage_per_day(self):
        return DayMapper(self.readings, self.device_map).map()

    @staticmethod
    def get_usage_per_event(events, readings):
        events_kwh = {}
        i = 0
        while i < len(events):
            if i+1 >= len(events):
                break
            start_event = events[i]
            end_event = events[i+1]
            if not Avast.check_event_pair(start_event, end_event):
                i+=1
                continue

            device_id = start_event.device_id
            start_date = start_event.date
            end_date = end_event.date
            cycle_kwh = 0
            for reading in readings:
                if reading.device_id != device_id:
                    continue
                reading_date = Avast.correct_day(reading)
                if start_date <= reading_date <= end_date:
                    if Avast.scan_for_cost(reading.kwh):
                        cycle_kwh += reading.kwh
            events_kwh[device_id] = round(cycle_kwh,4)
            i+=2
        return events_kwh
        ## Avast nie uwzględnia eventów, które się zaczynają, ale nie kończą