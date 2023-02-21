"""
This functions create a map of film coordinations
"""
from math import radians, cos, sin, asin, sqrt
import argparse
import folium
from geopy.geocoders import Nominatim

def read_file(year,path):
    """
    reads file and sorts it by the given year
    """
    with open(path,"r",encoding="utf-8") as f:
        line = f.read().strip().split("\n")
    line = line[10:]
    lines = [i.split("\t") for i in line]
    lines = [i for i in lines for j in i if str(year) in j]
    return lines

def loc(lines):
    """
    get location of a film
    """
    coordinats = []
    geolocator = Nominatim(user_agent="locations")
    for i,j in enumerate(lines):
        if "(" in lines[i][-1]:
            if lines[i][-2].count(",") > 2:
                location = geolocator.geocode(lines[i][-2][lines[i][-2].index(",")+1:])
            else:
                location = geolocator.geocode(lines[i][-2])
        else:
            if lines[i][-1].count(",") > 2:
                location = geolocator.geocode(lines[i][-1][lines[i][-1].index(",")+1:])
            else:
                location = geolocator.geocode(lines[i][-1])
        coordinats.append([lines[i][0],location.latitude,location.longitude])
    return coordinats

def coor(coordinats,longtitude,latitude):
    """
    counts a distance between given coordinats and film coordinats
    """
    distance_film = []
    for i,j in enumerate(coordinats):
        longtitude1 = coordinats[i][-1]
        latitude1 = coordinats[i][-2]
        longtitude, latitude, longtitude1, latitude1 = \
        map(radians, [longtitude, longtitude, longtitude1, latitude1])
        dlon = longtitude1 - longtitude
        dlat = latitude1 - latitude
        distance = 2* asin(sqrt(sin(dlat/2)**2 + cos(latitude)\
         * cos(latitude1) * sin(dlon/2)**2))*6371
        distance_film.append([distance,coordinats[i]])
    return sorted(distance_film)[:10]

def make_map(distance_films):
    """
    creates a map
    """
    map_film = folium.Map()
    map_film = folium.Map(tiles = 'Stamen Terrain')
    fg_market = folium.FeatureGroup(name="icons")
    fg_circle = folium.FeatureGroup(name="circle")
    for i,j in enumerate(distance_films):
        fg_market.add_child(folium.Marker(location=distance_films[i][1][1:],
                                    popup=distance_films[i][1][0],
                                    icon=folium.Icon('darkred')))
        fg_circle.add_child((folium.CircleMarker(location=distance_films[i][1][1:],
                                    popup=distance_films[i][1][0],
                                    fill_color = "blue")))
    map_film.add_child(fg_market)
    map_film.add_child(fg_circle)
    map_film.add_child(folium.LayerControl())
    map_film.save('Map_Stamen_Zoomed.html')
    return map_film

def main():
    """
    This function uses argperse to get an input
    """
    parser = argparse.ArgumentParser(description="creates map")
    parser.add_argument("year", type=int, help= "year of the films")
    parser.add_argument("longtitude", type=float, help= "coordinats")
    parser.add_argument("latitude", type=float, help= "coordinats")
    parser.add_argument("path", type=str, help= "path to dataset")

    args = parser.parse_args()
    print(make_map(coor(loc(read_file(args.year,args.path)),args.latitude,args.longtitude)))

if __name__ == "main":
    main()
