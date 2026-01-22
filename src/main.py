from data.rawdata import DATASET
from make_object import *
from usage import *
from cost import *
from efficiency import *
def text_kwh(dane):
    for id, info in dane.items():
        print(f"Dla {id} zużycie wyniosło: {info}kWh.")
def text_pln(dane):
    for id, info in dane.items():
        print(f"Dla {id} koszt to: {info}zł.")
def text_damaged(dane):
    for id, info in dane.items():
        print(f"Urządzenie {id} jest uszkodzone, ponieważ przekroczono wydajność rzędu 100%")
devices = [Device.from_dict(d) for d in DATASET["devices"]]
households = [Household.from_dict(h) for h in DATASET["household"]]
events = [Event.from_dict(e) for e in DATASET["events"]]
readings = [Reading.from_dict(r) for r in DATASET["readings"]]

usage= Usage(readings, devices, households)
calc = Calculator()
eff = EfficiencyChecker()

print("I Analiza - Zużycie i koszt na urządzenie")
print(20*"-")
text_kwh(usage.get_usage_per_device())
print(20*"-")
text_pln(calc.calculate(usage.get_usage_per_device()))
print(20*"-")

print("II Analiza - Zużycie i koszt na domownika. Everyone -> Część wspólna zużycia. W koszcie została uwzględniona dla każdego już")
print(20*"-")
text_kwh(usage.get_usage_per_household())
print(20*"-")
text_pln(calc.calculate(usage.get_usage_per_household()))
print(20*"-")

print("III Analiza - Zużycie i koszt na pomieszczenie")
print(20*"-")
text_kwh(usage.get_usage_per_room())
print(20*"-")
text_pln(calc.calculate(usage.get_usage_per_room()))
print(20*"-")

print("IV Analiza - Zużycie i koszt na dzień")
print(20*"-")
text_kwh(usage.get_usage_per_day())
print(20*"-")
text_pln(calc.calculate(usage.get_usage_per_day()))
print(20*"-")

print("V Analiza - Zużycie i koszt na event")
print(20*"-")
text_kwh(usage.get_usage_per_event(events, readings))
print(20*"-")
text_pln(calc.calculate(usage.get_usage_per_event(events, readings)))
print(20*"-")

print("VI Analiza - Sprawdzenie, które urządzenie jest uszkodzone")
print(20*"-")
text_damaged(eff.map_status_to_obj(eff.get_avg_with_obj(readings, devices)))
print(20*"-")