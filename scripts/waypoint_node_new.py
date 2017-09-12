#!/usr/bin/env python
"""
These functions were copied from several different files in the mavros library.
These are modified code snippets of functions that are part of the larger mavros code base.
wp_load, see: https://github.com/mavlink/mavros/blob/master/mavros/scripts/mavwp
do_mode, see: https://github.com/mavlink/mavros/blob/master/mavros/scripts/mavsys
_arm, see: https://github.com/mavlink/mavros/blob/master/mavros/scripts/mavsafety
"""
from __future__ import print_function
import rospy
import sys
import mavros
import argparse
import threading

from mavros.utils import *
from mavros import mission as M
#from mavros.mission import push as Mpush
from mavros_msgs.srv import SetMode
from mavros import command
from mavros_msgs.msg import State
from geographic_msgs.msg import GeoPoint
from std_msgs.msg import Float64
from soi_waypoint_work.msg import LatLongWayptList

# load waypoints
def get_wp_file_io(args):
#def get_wp_file_io():
    return M.QGroundControlWP()

def do_load(args):
#def do_load(filename_str):
    """ filename_str is the file location (and filename) to open that has the waypoints
    we are also assuming that we are not preserving the home location """
#def do_load(waypoint_list):
    """ waypoint_list is expected to be in a "list of Waypoint[(s)]" format
    (from mavros_msgs.msg import Waypoint)
    we are also assuming that we are not preserving the home location """

    wps = []
    wps_file = get_wp_file_io(args)
    #wps_file = get_wp_file_io()
    with args.file:
        wps = [w for w in wps_file.read(args.file)]
    #with filename_str:
    #    wps = [w for w in wps_file.read(filename_str)]
    print("wps is %r" % wps)

    # this is from _load_call(waypoint_list)
    #try:
    #    ret = M.push(waypoints=wps)
    #except rospy.ServiceException as ex:
    #    fault(ex)

    def _load_call(waypoint_list):
        print("waypoint_list is: %r" % str(waypoint_list))
        print("M.push is... %r" % str(M.push))
        #print("Mpush is... %r" % str(Mpush))
        try:
            ret = M.push(waypoints=waypoint_list)
        except rospy.ServiceException as ex:
            fault(ex)

        if not ret.success:
            fault("Request failed. Check mavros logs")

        print_if(args.verbose, "Waypoints transfered:", ret.wp_transfered)

    done_evt = threading.Event()
    def _fix_wp0(topic):
        if len(topic.waypoints) > 0:
            wps[0] = topic.waypoints[0]
            print_if(args.verbose, "HOME location: latitude:", wps[0].x_lat,
                     "longitude:", wps[0].y_long, "altitude:", wps[0].z_alt)
        else:
            print("Failed to get WP0! WP0 will be loaded from file.", file=sys.stderr)

        done_evt.set()

    if not args.preserve_home:
        print("not args.preserve_home")
        _load_call(wps)
    else:
        print("args.preserve_home")
        # Note: _load_call() emit publish on this topic, so callback only changes
        # waypoint 0, and signal done event.
        sub = M.subscribe_waypoints(_fix_wp0)
        if not done_evt.wait(30.0):
            fault("Something went wrong. Topic timed out.")
        else:
            sub.unregister()
            _load_call(wps)



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
    state = 1 # true, throttle on
    try:
        ret = command.arming(value=state)
    except rospy.ServiceException as ex:
        fault(ex)

    if not ret.success:
        fault("Request failed. Check mavros logs")

    #print_if(args.verbose, "Command result:", ret.result)
    print("Command result:", ret.result)
    return ret

#defining the class
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
        thedata = None
        self.lock.acquire()
        try:
            thedata = self.myGeoPoint
            self.myGeoPoint = None
        finally:
            self.lock.release()
        #print("Data2 received: %r" % thedata)
        return thedata
    

    def received_rawdata(self):
        """
        input: (none)
        output: thedata (std_msgs.msg.String)
        
        returns raw data that was received,
        in its original ROS format
        """
        self.thedata
        self.lock.acquire()
        try:
            thedata = self.myGeoPoint_ros
            self.myGeoPoint_ros = LatLongWayptList()
        finally:
            self.lock.release()
        return thedata
    

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

        thedata = None
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
        thedata = None
        self.lock.acquire()
        try:
            thedata = self.myfloat64_ros
            self.myfloat64_ros = Float64()
        finally:
            self.lock.release()
        return thedata


# defining waypoint_node_new
def waypoint_node_new():
    rospy.init_node('waypoint_node_new', anonymous=True)

    # to determine whether we'll need to force a takeoff first
    # before passing along the waypoints, we look at the altitude measurement
    # (this assumes that we start at the set landing strip and start location
    # and also that we will never dip below this altitude later (no landing command)
    # -- this sort-of works, because UxAS is for flight between takeoff and landing only)
    # thus, looking at the altitude measurement effectively tells us whether
    # we've taken off yet or not, so we need to test altitude height;
    # we get the data via the mavros interface:
    float64_in = Float64Data()
    rospy.Subscriber("/mavros/global_position/rel_alt", Float64, float64_in.callback)

    GeoPoint_in = LatLongWayptListData()
    rospy.Subscriber("/UAV1/testGeoPoint", LatLongWayptList, GeoPoint_in.callback)
    #rospy.Subscriber("/UAV1/waypoint_list", soi_waypoint_work/LatLongWayptList, waypoints_in.callback)

    print("Waiting for incoming ROS topic data...")

    counter = 0
    hold_alt = None
    while hold_alt is None: # need an init alt before get waypt list, otherwise could skip and overwrite a received waypt list with a None below
        hold_alt = float64_in.received_data()
    while (1):
        hold = float64_in.received_data() # we DON'T overwrite the old data!
        if hold is None:
            pass
        else: # we have new data and only update when we have a new altitude measurement
            hold_alt = hold # the most recent data received is saved
            print("Data received: %r" % hold_alt)
        hold2 = GeoPoint_in.received_data()
        if hold2 is None:
            pass
        else: # we have new data
            print("Data2 received: %r" % hold2)
            #print(hold2[1].latitude)
        #hold2 = 1 # comment out when reading GeoPoint_in
        if not (hold_alt is None) and not (hold2 is None): # at this stage, need hold_alt and Waypt list, and will always have some altitude measurement (due to prior loop before this one)

            # file write-out
            #fh = open("/$HOME/ardupilot/Tools/autotest/ArduPlane-Missions/hst.txt", 'w')
            fh = open("hst.txt", 'w')
            fh.write("QGC WPL 110\n")
            # this presumes that we're starting at this landing strip and location 
            #(lat=149.165085, long=-35.362938)
            if hold_alt < 0.3: # then we haven't takeoff yet, so give "takeoff"-type commands 
                #takeoff 00 position
                fh.write("0\t1\t0\t16\t0.000000\t0.000000\t0.000000\t0.000000\t-35.362938\t149.165085\t584.409973\t1\n")
                #takeoff 01 position
                fh.write("1\t0\t3\t22\t15.000000\t0.000000\t0.000000\t0.000000\t-35.361164\t149.163986\t28.110001\t1\n")
                counter = 2
                #firstwaypt = 0
            else: # we're already in the air, just get the next waypoint, don't print anything extra to file
                counter = 0
                #firstwaypt = 1
            
            for pt in hold2:
                longitude = pt.longitude
                latitude = pt.latitude
                altitude = pt.altitude
                fh.write("%d\t0\t3\t22\t15.000000\t0.000000\t0.000000\t0.000000\t%f\t%f\t%f\t1\n" % (counter, longitude, latitude, altitude))
                counter += 1
            fh.close()

            # do the service call stuff
            # and do file read-in and waypoint send
            #do_load("/home/turtlebot/ardupilot/Tools/autotest/ArduPlane-Missions/hst.txt")
            #filenamestr = ["mavwp", "load", "/home/turtlebot/ardupilot/Tools/autotest/ArduPlane-Missions/hst.txt"]
            filenamestr = ["mavwp", "load", "hst.txt"]

            parser = None # forcibly overwrite previous
            parser = argparse.ArgumentParser(description="Command line tool for manipulating mission on MAVLink device.")
            parser.add_argument('-n', '--mavros-ns', help="ROS node namespace", default="/mavros")
            parser.add_argument('-v', '--verbose', action='store_true', help="verbose output")
            subarg = None # forcibly overwrite previous
            subarg = parser.add_subparsers()
            load_args = subarg.add_parser('load', help="load waypoints from file")
            load_args.set_defaults(func=do_load)
            load_args.add_argument('-p', '--preserve-home', action='store_true', help="Preserve home location (WP 0, APM only)")
            load_args.add_argument('file', type=argparse.FileType('rb'), help="input file (QGC/MP format)")
            #args = parser.parse_args(rospy.myargv(argv=sys.argv)[1:])
            args = parser.parse_args(rospy.myargv(argv=filenamestr)[1:])

            mavros.set_namespace(args.mavros_ns) # necessary for M.push to be registered by M._setup_services()

            args.func(args) # the filenamestr will forcibly call the do_load() function

            do_mode() # has to be put into AUTO mode post-waypoint send (or will reset to RTL mode)

            if hold_alt < 0.3:
                _arm()   # arm only when on ground
            else:
                pass
            
            
        #break # comment this out for loop (not single-run)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

"""
opened_file.open(filename, 'w')
opened_file.write("QGC WPL 110")

#takeoff 00 position
opened_file.write("0\t1\t0\t16\t0.000000\t0.000000\t0.000000\t0.000000\t-35.362938\t149.165085\t584.409973\t1")

#takeoff 01 position
opened_file.write("1\t0\t3\t22\t15.000000\t0.000000\t0.000000\t0.000000\t-35.361164\t149.163986\t28.110001\t1")

firstwaypt = 0; counter = 0
for pt in waypts:
    [longitude,latitude,altitude] = pt
    if firstwaypt == 0:                       # with constant unchanging orientation
        opened_file.write("%d\t0\t3\t16\t0.000000\t1.000000\t0.000000\t0.000000\t%d\t%d\t%d\t1\n" % (counter, longitude, latitude, altitude))
    firstwaypt = 1
    else:                                # with constant unchanging orientation
        opened_file.write("%d    0   3   22  15.000000   0.000000    0.000000    0.000000    %d  %d  %d  1\n" % (counter, longitude, latitude, altitude))
    counter += 1
opened_file.close()
"""



if __name__ == '__main__':
  
#    try:
#        waypoint_node_new()
    #except rospy.shutdown(): #ROSError??? etc.:
    #    sys.exit()
#    except:
#        pass
    waypoint_node_new()

    sys.exit(0)            
