from typing import List

from classes.Sector import Sector


class Airspace:
    def __init__(self, id: str, group: str, owner: List[str], sectors: List[Sector]):
        self.id = id
        self.group = group
        self.owner = owner
        self.sectors = sectors


def find_airspace_by_owner(airspace_list: List[Airspace], sector: str) -> Airspace:
    for airspace_object in airspace_list:
        if airspace_object.owner[0] == sector:
            return airspace_object
    return None
