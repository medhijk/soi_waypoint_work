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
class WaypointData(object):
    def __init__(self):
        self.waypoint = None #"" # unpacked
        self.waypoint_ros = String() # raw format
        self.lock = threading.Lock()

    def callback(self, data):
        self.lock.acquire()
        try: # this looks different depending on the datatype
            self.waypoint = data.LatLongWayptList # data is expected to be in LatLongWayptList format
            self.waypoint_ros = data
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
            thedata = self.waypoint
            self.waypoint = None
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
            thedata = self.waypoint_ros
            self.waypoint_ros = String()
        finally:
            self.lock.release()
        return thedata
    
        
        
            
