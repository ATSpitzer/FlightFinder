from Page_Explorer.Edreams.FlightSearch_Explorer import FlightSearch
from Page_Explorer.Edreams.FlightResults_Explorer import FlightResults

shortcut_string="https://www.edreams.com/travel/#results/type=R;from=CGK;to=LOP;dep=2020-07-19;ret=2020-07-25;buyPath=FLIGHTS_HOME_SEARCH_FORM;internalSearch=true"
    # "https://www.edreams.in/travel/#results/type=R;from=CGK;to=LOP;dep=2020-07-19;ret=2020-07-25;buyPath=FLIGHTS_HOME_SEARCH_FORM;internalSearch=true"


ff = FlightSearch(start_url="http://www.edreams.in")
ff.check_url()
ff.search_flight_rt(start='CGK',end='LOP',date1="July 19 20",date2="July 25 20")

fr_driver=ff.get_driver_object()
fr = FlightResults(driver_element=ff.get_driver_object())
fr.check_url(screenshot=True, screenshot_name='from_in_home.png')

fr2 = FlightResults(start_url=shortcut_string)
fr2.check_url(screenshot=True, screenshot_name='from_com_search.png')
fr2.close_driver()