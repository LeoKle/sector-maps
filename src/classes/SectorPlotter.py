from data.fetchData import fetch_data
from data.settings import load_sector_settings
from classes.convertObject import convert_objects_to_airspace
from plotting.plotSector import create_sector_plot


class SectorPlotter:
    def __init__(self):
        # load vatglasses data
        self.vatglasses_data = fetch_data()
        airspace_data = self.vatglasses_data.get("airspace")
        self.airspaces = []
        for element in airspace_data:
            airspace = convert_objects_to_airspace(element)

            self.airspaces.append(airspace)

        # import sector plotting settings
        self.sector_settings = load_sector_settings()

    def plot_sectors(self):
        for sector in self.sector_settings:
            create_sector_plot(sector, self.airspaces)
