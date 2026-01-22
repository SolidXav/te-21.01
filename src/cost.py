from avast import *
class Calculator:
    def __init__(self, price_per_kwh=0.89):
        self.price_per_kwh = price_per_kwh

    def per_person(self, usage_per_person):
        ## Uwzględnia koszty zużycia na pokój danej osoby + uwzględnia wspólne zużycie i dzieli na 3 domowników
        return {person_id: round(self.price_per_kwh*(kwh+usage_per_person["Everyone"]/3),2)
                for person_id, kwh in usage_per_person.items()
                if person_id != "Everyone"}

    def calculate(self, usage):
        return {id: round(kwh* self.price_per_kwh, 2) for id, kwh in usage.items()}