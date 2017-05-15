from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from sklearn.cluster import KMeans

def load_asc(filename):
    fp = open(filename)

    ncols, count = fp.readline().split()
    ncols = int(count)

    nrows, count = fp.readline().split()
    nrows = int(count)

    xllcorner, value = fp.readline().split()
    xllcorner = float(value)

    yllcorner, value = fp.readline().split()
    yllcorner = float(value)

    cellsize, value = fp.readline().split()
    cellsize = float(value)

    NODATA_value, value = fp.readline().split()
    NODATA_value = float(value)

    data = []

    for line in fp:
        fields = line.strip().split()
        data.append([float(field) for field in fields])


    data = np.array(data)
    data[data==NODATA_value] = 0

    return data, xllcorner, yllcorner, cellsize

def map_points(xllcorner, yllcorner, cellsize, nrows, x, y):
    x = int((x-xllcorner)/cellsize)
    y = (nrows-1)-int((y-yllcorner)/cellsize)

    return x, y

def load_airports(filename):
    airports = {}

    for line in open("airport_gps.dat"):
            fields = line.strip().split()

            airport_id = int(fields[0])
            lat = float(fields[1])
            lon = float(fields[2])

            airports[airport_id] = (lat, lon)

    return airports

pop, xllcorner, yllcorner, cellsize = load_asc('US_pop.asc')
airports = load_airports('airport_gps.dat')
coords = np.array(list(airports.values()))
nrows = pop.shape[0]
ncols = pop.shape[1]

seeds = []

for i in range(coords.shape[0]):
    x, y = map_points(xllcorner, yllcorner, cellsize, nrows, coords[i][1], coords[i][0])

    if x <0  or x>= ncols:
        continue

    if y <0 or y >= nrows:
        continue

    if pop[y, x] > 0:
        seeds.append((x,y))

seeds = np.array(seeds)

positions = np.zeros((nrows*ncols, 2), dtype='int')

count = 0
for i in range(nrows):              
    for j in range(ncols):                                                                     
        positions[count][0] = j                                                                
        positions[count][1] = i
        count += 1

kmeans = KMeans(n_clusters=seeds.shape[0], init=seeds, n_init=1, max_iter=1)
kmeans.fit(positions)

basins = np.zeros((nrows, ncols), dtype='int')

for i in range(len(kmeans.labels_)):          
    basins[positions[i][1]][positions[i][0]] = kmeans.labels_[i]

plt.imshow(basins, cmap=cm.coolwarm)
plt.savefig('basins.png')
