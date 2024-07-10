import dataclasses
from typing import NewType


@dataclasses.dataclass
class Race:
    pass


CarId = NewType("CarId", int)
DriverId = NewType("DriverId", int)


def get_car_id(brand: str) -> CarId:
    return CarId(0)


def get_driver_id(name: str) -> DriverId:
    return DriverId(0)


def race(car: CarId, driver: DriverId) -> Race:
    return Race()


car = get_car_id("Mazda")
driver = get_driver_id("Stig")
race = race(driver, car)
