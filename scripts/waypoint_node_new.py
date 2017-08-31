#!/usr/bin/env python
"""
These functions were copied from several different files in the mavros library.
These are modified code snippets of functions that are part of the larger mavros code base.
wp_load, see: https://github.com/mavlink/mavros/blob/master/mavros/scripts/mavwp
do_mode, see: https://github.com/mavlink/mavros/blob/master/mavros/scripts/mavsys
_arm, see: https://github.com/mavlink/mavros/blob/master/mavros/scripts/mavsafety
"""
import rospy
import sys
import mavros
import argparse
import threading

from mavros import mission as M
from mavros_msgs.srv import SetMode
from mavros import command

# load waypoints
#def get_wp_file_io(args):
def get_wp_file_io():
    return M.QGroundControlWP()

def do_load(filename_str):
    """ filename_str is the file location (and filename) to open that has the waypoints
    we are also assuming that we are not preserving the home location """
#def do_load(waypoint_list):
#    """ waypoint_list is expected to be in a "list of Waypoint[(s)]" format
#    (from mavros_msgs.msg import Waypoint)
#    we are also assuming that we are not preserving the home location """

    wps = []
    #wps_file = get_wp_file_io(args)
    wps_file = get_wp_file_io()
    #with args.file:
        #wps = [w for w in wps_file.read(args.file)]
    with filename_str:
        wps = [w for w in wps_file.read(filename_str)]
    #print("wps is %r" % wps)

    # this is from _load_call(waypoint_list)
    try:
        ret = M.push(waypoints=wps)
    except rospy.ServiceException as ex:
        fault(ex)

# set mode
#def do_mode(args):
def do_mode():
    """ for this use case, custom_mode is always expected to be 'AUTO' """
    base_mode = 0
    #custom_mode = ''
    custom_mode = 'AUTO'

    try:
        set_mode = rospy.ServiceProxy(mavros.get_topic('set_mode'), SetMode)
        ret = set_mode(base_mode=base_mode, custom_mode=custom_mode)
    except rospy.ServiceException as ex:
        fault(ex)

# arm plane
#def _arm(args, state):
def _arm():
    """ for this use case, state is always expected to be 'throttle' """
    state = 'throttle'
    try:
        ret = command.arming(value=state)
    except rospy.ServiceException as ex:
        fault(ex)

    if not ret.success:
        fault("Request failed. Check mavros logs")

    #print_if(args.verbose, "Command result:", ret.result)
    print("Command result:", ret.result)
    return ret

# defining the class
class LatLongWayptListData(object):
    def __init__(self):
        self.myGeoPoint = None #"" # unpacked
        self.myGeoPoint_ros = LatLongWayptList() # raw format
        self.lock = threading.Lock()

    def callback(self, data):
        self.lock.acquire()
        try: # this looks different depending on the datatype
            self.myGeoPoint = data.geopoints # data is expected to be in LatLongWayptList format
            self.myGeoPoint_ros = data
        finally:
            self.lock.release()

    def received_data(self):
        """
        input: (none)
        output: thedata (string)
        
        returns unpacked data that was received,
        NOT in its original ROS format
        """
        self.lock.acquire()
        try:
            thedata = self.myGeoPoint
            self.myGeopoint = None
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
            thedata = self.myGeoPoint_ros
            self.myGeoPoint_ros = LatLongWayptList()
        finally:
            self.lock.release()
        return thedata
    
# defining waypoint_node_new
def waypoint_node_new():

    rospy.init_node('waypoint_node_new', anonymous=True)
    GeoPoint_in = LatLongWayptListData()
    rospy.Subscriber("/UAV1/testGeoPoint", soi_waypoint_work/LatLongWayptList, GeoPoint_in.callback)
    #rospy.Subscriber("/UAV1/waypoint_list", soi_waypoint_work/LatLongWayptList, waypoints_in.callback)

    print("Waiting for incoming ROS topic data...")

    while (1):
        #hold = string_in.received_data()
        #if hold is None:
        #    pass
        #else: # we have new data
        #    print("String received: %r" % hold)
        hold2 = GeoPoint_in.received_data()
        if hold2.data is None:
            pass
        else: # we have new data
            print("Data2 received: %r" % hold2)
        
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
  
    try:
        waypoint_node_new()
    #except rospy.shutdown(): #ROSError??? etc.:
    #    sys.exit()
    except:
        pass

    sys.exit(0)            
