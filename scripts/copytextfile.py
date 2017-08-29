#!/usr/bin/env python
import rospy
import sys
import json

# Read second line of data topic_info.txt

with open("topic_info.txt", "r") as f:
    data = f.readlines()
    for line in data:
        words = line.split(",") 



# convert list into float
new_list = [float(i) for i in words]


#final_list = [0, new_list[14], new_list[12], new_list[13], new_list[16], new_list[17], new_list[18], new_list[19], new_list[20], new_list[21], new_list[22], new_list[15]]


#print( ", ".join( str(e) for e in final_list ) )
seq=2
current=new_list[3]
frame=new_list[1]
command=new_list[2]
param1=new_list[5]
param2=new_list[6]
param3=new_list[7]
param4=new_list[8]
x=new_list[9]
y=new_list[10]
z=new_list[11]
autocontinue=new_list[4]
#################################################

missionlist = final_list
fh = open("hst.txt", "w")
output='QGC WPL 110\n'
#for cmd in missionlist:
commandline="%d\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\n" %(seq,current,frame,command,param1,param2,param3,param4,x,y,z,autocontinue)

takeoff_zero="0\t1\t0\t16\t0.000000\t0.000000\t0.000000\t0.000000\t-35.362938\t149.165085\t584.409973\t1\n"
takeoff_one="1\t0\t3\t22\t15.000000\t0.000000\t0.000000\t0.000000\t-35.361164\t149.163986\t28.110001\t1\n"
fh.write(output)
fh.write(takeoff_zero)
fh.write(takeoff_one)
fh.write(commandline)

fh.close()
# Create a new text file and copy data from topic_info.txt

"""
with open("hst.txt", "w") as outfile:
    json.dump(final_list[1,2], outfile)


#fh = open("hst.txt", "w")
#fh.write("%d" % words)
#fh.close()
"""
