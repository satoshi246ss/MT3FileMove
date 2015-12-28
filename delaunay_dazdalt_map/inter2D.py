from pylab import *
import numpy as np
from scipy import genfromtxt
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

#
import csv
fn='star_pos_data.txt'
print "Input:",fn
f = open(fn)
lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
f.close()
# lines2: リスト。要素は1行の文字列データ
fdaz  = open('daz.txt' , 'wb') 
fdalt = open('dalt.txt', 'wb') 
csvWriter_daz = csv.writer(fdaz)
csvWriter_dalt= csv.writer(fdalt)
count_data=0
for line in lines2:
    if line[0]=='#':
        continue
    count_data += 1
    az  = float(line[19:27])
    alt = float(line[27:35])
    daz = float(line[35:43])
    dalt= float(line[43:51])

    listData = []
    listData.append(az)                 #listにデータの追加
    listData.append(alt)
    listData.append(daz)
    csvWriter_daz.writerow(listData)    #1行書き込み

    listData2 = []
    listData2.append(az)                #listにデータの追加
    listData2.append(alt)
    listData2.append(dalt)
    csvWriter_dalt.writerow(listData2)  #1行書き込み
print "Obs Data Num.:",count_data
fdaz.close()
fdalt.close()

# ファイル読み込み
d = genfromtxt("daz.txt", delimiter=",")

points = d[:,0:2]
values = d[:,2]
grid_x, grid_y = np.mgrid[0:360, 0:90]

grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')

np.savetxt("grid_z1_az.txt",grid_z1)
plt.imsave("grid_z1_az",grid_z1)

#plt.imshow(grid_z1.T, extent=(0,360,0,90), origin='lower')
#plt.show()
print "OutPut:grid_z1_az.txt"
print "[0][0],[359][0],[0][89],[359][89] : ",grid_z1[0][0],grid_z1[359][0],grid_z1[0][89],grid_z1[359][89]

# ファイル読み込み
d = genfromtxt("dalt.txt", delimiter=",")

points = d[:,0:2]
values = d[:,2]
grid_x, grid_y = np.mgrid[0:360, 0:90]

grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')

np.savetxt("grid_z1_alt.txt",grid_z1)
plt.imsave("grid_z1_alt",grid_z1)

print "OutPut:grid_z1_alt.txt"
print "[0][0],[359][0],[0][89],[359][89] : ",grid_z1[0][0],grid_z1[359][0],grid_z1[0][89],grid_z1[359][89]
