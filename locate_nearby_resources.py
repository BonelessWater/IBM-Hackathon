import requests
from dotenv import load_dotenv
import os

load_dotenv()

def available_gas_stations(address: str, latitude: int, longitude: int, fuel_type="all"):
    api_key = os.getenv("FUEL_OUTAGE_API_KEY")
    service_url = f"https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key={api_key}&fuel_type={fuel_type}&radius=5&status=E&acces=public"
    if len(address) > 0:
        service_url += f"&location={address}"
    elif -90 <= latitude <= 90 and -180 <= longitude <= 180:
        service_url += f"&longitude={longitude}&latitude={latitude}"
    response = requests.get(service_url)

    stations = []
    if response.status_code == 200: 
        data = response.json()
        if "fuel_stations" in data:
            
            for station in data["fuel_stations"]:
                name_station=station.get("station_name", "N/A")
                latitude_station= station.get("latitude", "N/A")
                longitude_station=station.get("longitude", "N/A")
                add=True
                for s in stations:
                    if abs(latitude_station - s['latitude']) < 0.001 and abs(longitude_station - s['longitude']) < 0.0008:
                        add=False
                if add:
                    distance_station=distance_addresses(coordinates_origin=(latitude, longitude), coordinates_destination=(latitude_station, longitude_station))
                    address_station=station.get("street_address", "N/A")
                    if address_station == "N/A":
                        address_station = latlong_to_location(latitude_station, longitude_station)
                    fuel=station.get("fuel_type_code", "N/A")
                    stations.append({"name": name_station, "address": address_station, "latitude": latitude_station, "longitude":longitude_station,  "distance":distance_station, "fuel_type":fuel})
            return stations
    return stations


def hospital_finder(latitude: int, longitude: int):
    location = f"{latitude}, {longitude}"
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    place = "hospital"
    radius = 5000  # in meters
    service_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={place}&key={api_key}"

    response = requests.get(service_url)
    if response.status_code == 200:
        hospitals = []
        data = response.json()
        for result in data['results']:
            hospital_name = result.get("name", "N/A")
            hospital_latitude = result['geometry']['location'].get("lat", "N/A")
            hospital_longitude = result['geometry']['location'].get("lng", "N/A")
            hospital_distance = distance_addresses(origin_address=(latitude, longitude), destination_address=(hospital_latitude, hospital_longitude))
            hospital_address = latlong_to_location(hospital_latitude, hospital_longitude)
            hospital = {"name": hospital_name, "address": hospital_address, "distance": hospital_distance}
            hospitals.append(hospital)
        return hospitals
    return None


def shelter_finnder(address: str, latitude: int, longitude: int, wheelchair_accesible=False) -> list:
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
    
    if wheelchair_accesible:
        service_url += f"{q_and}wheelchair_accesible{q_sep}'YES'"
    
    service_url += f"{q_and}shelter_status{q_sep}'OPEN'&outFields=*&outSR=4326&f=json"
    

    response = requests.get(service_url)

    shelters = []
    if response.status_code == 200:
        data = response.json()
        if 'features' in data:
            for shelter in data['features']: 
                shelter_name = shelter.get("shelter_name", "N/A")
                shelter_address = shelter.get("address", "N/A")
                shelter_distance = distance_addresses(address, shelter_address)
                shelters.append({"name": shelter_name, "address": shelter_address, "distance": shelter_distance})
            return shelters
    return None


def latlong_to_location(latitude: int, longitude: int) -> str:
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")

    service_url = f"https://maps.googleapis.com/maps/api/geocode/json"
    service_url += f"?latlng={latitude},{longitude}&key={api_key}"

    response = requests.get(service_url)
    if response.status_code == 200:
        data = response.json()
        return data['results'][0]['formatted_address']


def location_to_latlong(address: str) -> tuple:
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")

    print(address)
    address.replace(" ", "+")

    service_url = f"https://maps.googleapis.com/maps/api/geocode/json"
    service_url = f"?address={address}&key={api_key}"

    response = requests.get(service_url)
    if response.status_code == 200:
        data = response.json()
        location = data['results'][0]['geometry']['location']
        return (location['lat'], location['lng'])


def distance_addresses(origin_address="", destination_address="", coordinates_origin=(-10000, -10000), coordinates_destination=(-1000000, -100000)) -> str:
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")

    service_url = f"https://maps.googleapis.com/maps/api/distancematrix/json"
    o_lat, o_long = coordinates_origin
    d_lat, d_long = coordinates_destination
    if -90 <= o_lat <= 90 and -180 <= o_long <= 180 and -90 <= o_lat <= 90 and -180 <= o_long <= 180:
        service_url += f"?destinations={d_lat}%2C{d_long}&origins={o_lat}%2C{o_long}"
    elif len(origin_address) > 0 and len(destination_address) > 0:
        origin_address.replace(" ", "%20")
        origin_address.replace(",","%2C")
        destination_address.replace(" ", "%20")
        destination_address.replace(",", "%2C")
        service_url += f"?destinations={destination_address}&origins={origin_address}"
    service_url += f"&units=imperial&key={api_key}"

    response = requests.get(service_url)

    if response.status_code == 200:
        data = response.json()
        return data['rows'][0]['elements'][0]['distance']['text']
    