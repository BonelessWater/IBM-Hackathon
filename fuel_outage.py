import requests
from dotenv import load_dotenv
import os

load_dotenv()

def fuel_outages(location="", latitude=None, longitude=None):
    api_key = os.getenv("FUEL_OUTAGE_API_KEY")
    service_url = f"https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key={api_key}&location={location}&fuel_type=ALL&radius=5&status=E&acces=public"
    response = requests.get(service_url)

    if response.status_code == 200: 
        data = response.json()

        stations = []
        if "fuel_stations" in data:
            for station in data["fuel_stations"]:
                name=station.get("station_name", "N/A")
                latitude_station= station.get("latitude", "N/A")
                longitude_station=station.get("longitude", "N/A")
                stations.append({"Name": name, "latitude": latitude_station, longitude:longitude_station})
            return stations
        else:
            return None

