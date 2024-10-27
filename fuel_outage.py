import requests
from dotenv import load_dotenv
import os

load_dotenv()

def fuel_outages(location="",latitude=None, longitude=None, fuel_type="ALL", zip=None):
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
                stations.append({"Name": name, "latitude": latitude_station, "longitude":longitude_station, "fuel_type":fuel})
            return stations
    return stations

