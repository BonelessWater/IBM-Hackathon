import requests
from dotenv import load_dotenv
import os

load_dotenv()

def available_gas_stations(location="",latitude=-10000, longitude=-10000, zip=-10000, fuel_type="ALL") :
    api_key = os.getenv("FUEL_OUTAGE_API_KEY")
    service_url = f"https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key={api_key}&fuel_type={fuel_type}&radius=5&status=E&acces=public"
    if len(location) > 0:
        service_url += f"&location={location}"
    elif -90 <= latitude <= 90 and -180 <= longitude <= 180:
        service_url += f"&longitude={longitude}&latitude={latitude}"
    elif zip:
        service_url = f"&zip={zip}"
    response = requests.get(service_url)

    stations = []
    if response.status_code == 200: 
        data = response.json()

        if "fuel_stations" in data:
            for station in data["fuel_stations"]:
                name=station.get("station_name", "N/A")
                latitude_station= station.get("latitude", "N/A")
                longitude_station=station.get("longitude", "N/A")
                fuel=station.get("fuel_type_code", "N/A")
                stations.append({"name": name, "latitude": latitude_station, "longitude":longitude_station, "fuel_type":fuel})
            return stations
    return stations


def food_shelters(location="",latitude=-10000, longitude=-10000, zip=-10000):
    # TODO
    #api_key = os.getenv()
    ...

def hospitals(location="",latitude=-10000, longitude=-10000, zip=-10000):
    # TODO
    #api_key = os.getenv()
    ...

def shelters(city="", state="", latitude=-100000, longitude=-100000, zip=-10000, wheelchair_accesible=False):
    # doesnt need an api key
    service_url = f"https://gis.fema.gov/arcgis/rest/services/NSS/OpenShelters/MapServer/0/query?where="
    q_sep = f"%20%3D%20"
    q_and = f"%20AND%20"


    if -90 <= latitude <= 90 and -180 <= longitude <= 180:
        # sets the min and max latitude and longitude to represent all shelters within a radius of approx. 50 miles
        min_latitude, max_latitude = max(-90, latitude - 0.7), min(90, latitude + 0.7) # setting min and max latitude
        min_longitude, max_longitude = max(-180, longitude-0.9), min(180, longitude + 0.9) # setting min and max longitude
        
        service_url += f"%20(latitude{q_sep}{min_latitude}%20OR%20latitude{q_sep}{max_latitude})%20{q_and}"
        service_url += f"%20(longitude{q_sep}{min_longitude}%20OR%20longitude{q_sep}{max_longitude})%20"
    elif len(city) > 0:
        service_url += f"city{q_sep}'{city.upper()}'"
    elif zip > 0:
        service_url += f"zip{q_sep}'{zip}'"
    elif len(state) > 0:
        service_url += f"state{q_sep}'{state.upper()}'"
    
    if wheelchair_accesible:
        service_url += f"{q_and}wheelchair_accesible{q_sep}'YES'"
    
    service_url += f"{q_and}shelter_status{q_sep}'OPEN'&outFields=*&returnGeometry=false&outSR=4326&f=json"
    

    response = requests.get(service_url)

    shelters = []
    if response.status_code == 200:
        data = response.json()
        if 'features' in data:
            for shelter in data['features']: # works, but details to be discussed

                # future implementation
                '''
                shelter_name = shelter.get("shelter_name", "N/A")
                shelter_latitude = shelter.get("latitude", "N/A")
                shelter_longitude = shelter.get("longitude", "N/A")
                if shelter_latitude == "N/A" or shelter_longitude == "N/A":
                    shelter_address = shelter.get("address", "N/A")
                    shelter_city = shelter.get("city", "N/A")
                    shelter_latitude, shelter_longitude = location_to_latlong(shelter_address, shelter_city)
                
                shelters.append({"name": shelter_name, "latitude": shelter_latitude, "longitude": shelter_longitude})
                '''
                shelters.append(shelter)
            return shelters
    return None

# Possible future implementation, but requires geocoding API, check if watson has one
'''
def location_to_latlong(address, city):
    os.getenv()

'''
