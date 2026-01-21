from data.rawdata import DATASET
from make_object import *
from usage import *
devices = [Device.from_dict(d) for d in DATASET["devices"]]
households = [Household.from_dict(h) for h in DATASET["household"]]
events = [Event.from_dict(e) for e in DATASET["events"]]
readings = [Reading.from_dict(r) for r in DATASET["readings"]]

usage_service = Usage(
        readings=readings,
        device_list=devices,
        household_list=households
)

print(usage_service.give_me_that())