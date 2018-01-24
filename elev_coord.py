from geopy import Point
from geopy.distance import distance, VincentyDistance

lat = 50.0
lat_original = 50.0
long = 30.0

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
print lat_max[0]
print long_max[1]

#create a matrix
while True:
    if float(lat) >= float(lat_max[0]):
        print 'If option', lat, long
        long_string = grid_point_coordinate(distM,90,lat_original,long)
        long = long_string[1]
        lat = lat_original
    elif float(long) >= float(long_max[1]):
        print 'Elif option', lat, long
        break
    else:
        lat_string = grid_point_coordinate(distM,bearing,lat,long)
        lat = lat_string[0]
        print 'Else option', lat, long