from classes.Airspace import Airspace
from classes.Point import Point
from classes.Sector import Sector


def convert_objects_to_airspace(data):
    id_value = data.get("id")
    group = data.get("group")
    owner = data.get("owner")

    sectors = []
    for sector_data in data.get("sectors"):
        max_value = sector_data.get("max")
        min_value = sector_data.get("min")

        points = []
        for point_data in sector_data.get("points"):
            lat, long = map(str, point_data)
            points.append(Point(lat, long))

        sector = Sector(max_value, min_value, points)
        sectors.append(sector)

    return Airspace(id_value, group, owner, sectors)
