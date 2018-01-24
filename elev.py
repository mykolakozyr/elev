from geopy import Point
from geopy.distance import distance, VincentyDistance
import httplib
import urllib
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Parsing google for the elevation data in a particular place
def pars_google(a,b,c):

    url = 'https://maps.googleapis.com/maps/api/elevation/json?locations=' + str(a) + ',' + str(b) + '&key=' + c

    handler = requests.get(url, verify=False)
    result = handler.json()
    try:
        elev = result['results'][0]['elevation']
        lat = result['results'][0]['location']['lat']
        lng = result['results'][0]['location']['lng']
        return str(elev)+','+str(lat)+','+str(lng)
    except IndexError:
        print 'It seems like google does not like you'
        return 'NULL,'+str(a)+','+str(b)

output_file = open('output_3.csv', 'w')
output_file.write('elev,Y,X\n')
key = 'AIzaSyB037sWwaoGmdd98ZwJ-vfL30kKfw-mEQw'

lat = 50
lat_original = lat
long = 30

#function for new coordinate
def grid_point_coordinate(a,b,x,y):
    c = VincentyDistance(meters=int(a)).destination(Point(x, y), float(b)).format_decimal()
    c = c.split(',')
    return c

#define some metadata
distM = raw_input('Enter the distance between points (in meters): ')
dist_max = raw_input('Enter the total distance to be processed (in meters): ')
bearing = raw_input('Enter the bearing: ')

#find the bounds of interested area
lat_max = grid_point_coordinate(dist_max, 0, lat, long)
long_max = grid_point_coordinate(dist_max, 90, lat, long)

#find elevation data for the matrix
while True:
    if float(lat) >= float(lat_max[0]):
        data = pars_google(lat, long, key)
        output_file.write(data+'\n')
        print lat, long
        long_string = grid_point_coordinate(distM,90,lat_original,long)
        long = long_string[1]
        lat = lat_original
    elif float(long) >= float(long_max[1]):
        print 'We have ended. Thank you for participation'
        break
    else:
        data = pars_google(lat, long, key)
        output_file.write(data+'\n')
        lat_string = grid_point_coordinate(distM,bearing,lat,long)
        lat = lat_string[0]
        print lat, long