#!/usr/bin/env python

from __future__ import print_function
import rospy
import sys
import mavros
import argparse
import threading
from std_msgs.msg import Float64
from mavros.utils import*


#latitude = hold2[0].latitude
#longitude = hold2[0].longitude
#altitude = hold2[0].altitude

#latitude = 7
#longitude = 6
#altitude = 2



# read from /mavros/global_postition/rel_alt
# info is stored in data.data (is a std_msgs/Float64)
# set up the class and subscriber
#############################################################

#defining the class
class Float64Data(object):
    def __init__(self):
        self.myfloat64 = None #"" # unpacked
        self.myfloat64_ros = Float64() # raw format
        self.lock = threading.Lock()

    def callback(self, data):
        self.lock.acquire()
        try: # this looks different depending on the datatype
            self.myfloat64 = data.data # data is expected to be in Float64 format
            self.myfloat64_ros = data
        finally:
            self.lock.release()

    def received_data(self):

        self.thedata = None
        self.lock.acquire()
        try:
            thedata = self.myfloat64
            self.myfloat64 = None
        finally:
            self.lock.release()
        return thedata
    

    def received_rawdata(self):
        """
        input: (none)
        output: thedata (std_msgs.msg.String)
        
        returns raw data that was received,
        in its original ROS format
        """
        self.lock.acquire()
        try:
            thedata = self.myfloat64_ros
            self.myfloat64_ros = Float64()
        finally:
            self.lock.release()
        return thedata
    
# defining waypoint_node_new
def altitude_node_new():

    rospy.init_node('altitude_node_new', anonymous=True)
    float64_in = Float64Data()
    rospy.Subscriber("/mavros/global_position/rel_alt", Float64, float64_in.callback)
    #rospy.Subscriber("/UAV1/waypoint_list", soi_waypoint_work/LatLongWayptList, waypoints_in.callback)

    print("Waiting for incoming ROS topic data...")
    
    rospy.spin()
    
    while (1):
        #hold = string_in.received_data()
        #if hold is None:
        #    pass
        #else: # we have new data
        #    print("String received: %r" % hold)
        hold_alt = float64_in.received_data()
        if hold_alt is None:
            pass
        else: # we have new data
            print("Data received: %r" % hold_alt)
               
    
        
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()




##############################################################

#hold_alt = None
#while hold_alt is None: # loop until you get data from mavros
#    hold_alt = ???.received_data() # to be filled in
##############################################################

    fh = open("filename.txt", 'w')
    fh.write("QGC WPL 110\n")


# this presumes that we're starting at this landing strip and location (lat=149.165085, long=-35.362938)
    if hold_alt < 0.3: # then we haven't takeoff yet, so give "takeoff"-type commands 
    #takeoff 00 position
        fh.write("0\t1\t0\t16\t0.000000\t0.000000\t0.000000\t0.000000\t-35.362938\t149.165085\t584.409973\t1\n")
    #takeoff 01 position
        fh.write("1\t0\t3\t22\t15.000000\t0.000000\t0.000000\t0.000000\t-35.361164\t149.163986\t28.110001\t\n1")
    else: # we're already in the air =, just get the next waypoint
        pass

    firstwaypt = 0; counter = 2
#for pt in hold2:
##    [longitude, latitude, altitude] = pt
#   latitude = t.latitude
#   longitude = pt.longitude
#   altitude = pt.altitude
    #if firstwaypt == 0:                       # with constant unchanging orientation
    #    opened_file.write("%d    1   0   22  15.000000   0.000000    0.000000    0.000000    %d  %d  %d  1\n" % (counter, longitude, latitude, altitude))
    #firstwaypt = 1
    #else:                                # with constant unchanging orientation
    fh.write("%d    0   3   22  15.000000   0.000000    0.000000    0.000000    %f  %f  %f  1\n" % (counter, longitude, latitude, altitude))
    #counter += 1
    fh.close()
    
    rospy.spin()    

