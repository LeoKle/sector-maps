import os
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np


from classes.Airspace import find_airspace_by_owner
from classes.DataProvider import DataProvider
from utils.coordinates import convertLat, convertLong
from utils.convertObject import convert_objects_to_airspace


class SectorPlotter:
    """Plots sectors, neighbouring sectors"""

    def __init__(self):
        # load vatglasses data
        self.vatglasses_data = DataProvider().load_vatglasses_data()
        airspace_data = self.vatglasses_data.get("airspace")
        self.airspaces = []
        for element in airspace_data:
            airspace = convert_objects_to_airspace(element)

            self.airspaces.append(airspace)

        # import sector plotting settings
        self.sector_settings = DataProvider().load_sector_settings()

    def plot_sectors(self):
        for sector in self.sector_settings:
            self.create_sector_plot(sector, self.airspaces)

    def plot_subsectors(self, ax, airspace, border_color="grey", fill_color="grey"):
        for subsector in airspace.sectors:
            # Extract latitudes and longitudes from sector's points
            latitudes = [convertLat(point.lat) for point in subsector.points]
            longitudes = [convertLong(point.long) for point in subsector.points]

            latitudes.append(latitudes[0])
            longitudes.append(longitudes[0])

            # Convert latitudes and longitudes to map coordinates
            x, y = self.m(longitudes, latitudes)

            # Plot the sector
            ax.plot(x, y, linewidth=0.5, c=border_color)
            ax.fill(x, y, alpha=0.05, c=fill_color)

    def create_sector_plot(self, sector, airspaces):
        sector_name = sector.get("sector_to_plot")
        sector_airspace = find_airspace_by_owner(airspaces, sector_name)
        neighbours_airspaces = []

        if sector_airspace is None:
            return

        def find_center_coords():
            total_lat = 0
            total_lon = 0
            total_points = 0

            # coordinates of main sector
            for subsector in sector_airspace.sectors:
                for point in subsector.points:
                    total_lat += convertLat(point.lat)
                    total_lon += convertLong(point.long)
                    total_points += 1

            neighbours = sector.get("neighbours")

            for neighbour in neighbours:
                neighbour_airspace = find_airspace_by_owner(airspaces, neighbour)
                if neighbour_airspace is not None:
                    neighbours_airspaces.append(neighbour_airspace)
                    for subsector in neighbour_airspace.sectors:
                        for point in subsector.points:
                            total_lat += convertLat(point.lat)
                            total_lon += convertLong(point.long)
                            total_points += 1

            if total_points == 0:
                return 0, 0
            else:
                center_lat = total_lat / total_points
                center_lon = total_lon / total_points

                return center_lat, center_lon

        fig, ax = plt.subplots(nrows=1, ncols=1)
        center_lat, center_lng = find_center_coords()

        self.m = Basemap(
            width=1,
            height=1,
            resolution="l",
            projection="stere",
            lat_0=center_lat,
            lon_0=center_lng,
        )

        # Plot subsectors
        for neighbour_airspace in neighbours_airspaces:
            self.plot_subsectors(
                ax, neighbour_airspace, border_color="grey", fill_color="grey"
            )

        # Plot main sector
        self.plot_subsectors(
            ax, sector_airspace, border_color="orange", fill_color="orange"
        )

        scale = sector.get("scale") if sector.get("scale") is not None else 0
        x_min, x_max = ax.get_xlim()
        x_shift = np.abs((x_max - x_min) / 2)
        y_min, y_max = ax.get_ylim()
        y_shift = np.abs((y_max - y_min) / 2)
        ax.set_xlim((x_min - scale * x_shift, x_max + scale * x_shift))
        ax.set_ylim((y_min - scale * y_shift, y_max + scale * y_shift))
        ax.set_aspect("equal", adjustable="box")
        ax.axis(False)

        title = (
            sector.get("title") if sector.get("title") is not None else "VATSIM Germany"
        )
        plt.title(f"{title}", horizontalalignment="center")

        # save the map
        new_path = os.path.relpath(sector.get("folder_path"), "data")
        plt.savefig(new_path + "\\" + sector_name + ".svg")
