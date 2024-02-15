def convertLat(lat):
    if lat.startswith("-"):
        lat_sign = -1
    else:
        lat_sign = 1

    lat_degrees, lat_minutes, lat_seconds = split_Lat(lat)

    lat_num = (lat_degrees + lat_minutes / 60 + lat_seconds / 3600) * lat_sign

    return lat_num


def convertLong(long):
    if long.startswith("-"):
        lng_sign = -1
    else:
        lng_sign = 1

    lng_degrees, lng_minutes, lng_seconds = split_Long(long)

    lng_num = (lng_degrees + lng_minutes / 60 + lng_seconds / 3600) * lng_sign

    return lng_num


def split_Lat(str):
    first_part = int(str[:2])
    second_part = int(str[2:4])
    third_part = int(str[4:])
    return first_part, second_part, third_part


def split_Long(str):
    first_part = int(str[:3])
    second_part = int(str[3:5])
    third_part = int(str[5:])

    return first_part, second_part, third_part


def find_center_coords(sector):
    total_lat = 0
    total_lon = 0
    total_points = 0

    # coordinates of main sector
    for subsector in sector.sectors:
        for point in subsector.points:
            total_lat += convertLat(point.lat)
            total_lon += convertLong(point.long)
            total_points += 1

    if total_points == 0:
        print("0, 0")
        return 0, 0
    else:
        center_lat = total_lat / total_points
        center_lon = total_lon / total_points

        print(center_lat, center_lon)
        return center_lat, center_lon
