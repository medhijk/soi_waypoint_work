#!/usr/bin/env python

import rospy
import sys
import mavros
import argparse
import threading

# load waypoints
def wp_load(waypoint_list)
        try:
            ret = M.push(waypoints=waypoint_list)
        except rospy.ServiceException as ex:
            fault(ex)

# set mode
def do_mode(args):
    base_mode = 0
    custom_mode = ''

    try:
        set_mode = rospy.ServiceProxy(mavros.get_topic('set_mode'), SetMode)
        ret = set_mode(base_mode=base_mode, custom_mode=custom_mode)
    except rospy.ServiceException as ex:
        fault(ex)

# arm plane
def _arm(args, state):
    try:
        ret = command.arming(value=state)
    except rospy.ServiceException as ex:
        fault(ex)

    if not ret.success:
        fault("Request failed. Check mavros logs")

    print_if(args.verbose, "Command result:", ret.result)
    return ret
        
        
            
