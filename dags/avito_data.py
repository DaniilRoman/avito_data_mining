from typing import Optional, List
from dataclasses import dataclass, fields, astuple

import context

@dataclass
class AvitoFlat():
    href: str
    apartment_type: str
    price: int
    address: str
    square: float
    building_floor: int
    flat_floor: int
    commission_percent: Optional[int]
    time_of_creation: str
    agency: Optional[str]
    metro_distance: Optional[str]
    metro_station: Optional[str]

    def as_tuple(self):
        return astuple(self)

    @staticmethod
    def get_fields():
        return [field.name for field in fields(AvitoFlat)]


@dataclass
class ParseException:
    msg: str
    context: Optional[object] = None

exceptions: List[ParseException] = []

class CatchError:
    def __init__(self, msg):
        self.msg = msg

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try: 
                result = func(*args, **kwargs)
                return result
            except Exception:
               print(self.msg)
               exceptions.append(ParseException(self.msg, str(args[1])))
        return wrapper

class SaveExceptions:
    def __init__(self, msg):
        self.msg = msg

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if (len(exceptions) != 0):
                context.store.save_exceptions(exceptions)
                raise Exception(self.msg)
            return result
        return wrapper

if __name__ == "__main__":
    print("its works")