from Page_Explorer.Trip.TripResults_Explorer import TripResultsExplorer
from Page_Explorer.Trip.locators import HotelSearchLocators as h
te = TripResultsExplorer()
res = te.build_results()
for r in res:
    print(r)