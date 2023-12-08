from typing import List

from classes.Sector import Sector


class Airspace:
    def __init__(
        self, airspace_id: str, group: str, owner: List[str], sectors: List[Sector]
    ):
        self.airspace_id = airspace_id
        self.group = group
        self.owner = owner
        self.sectors = sectors


def find_airspace_by_owner(airspace_list: List[Airspace], sector: str) -> Airspace:
    for airspace_object in airspace_list:
        if airspace_object.owner[0] == sector:
            return airspace_object
    return None
