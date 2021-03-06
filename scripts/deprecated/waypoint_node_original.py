#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String

#def callback(data):
#    rospy.loginfo(rospy.get_caller_id() + "heard %s", data.data)

import threading

"""
This is the automated version of running the following commands at the command line
and/or inside the MAVLink autopilot terminal, with MAVLink + roscore + mavros already running:

<PUT IN COMMANDS FOR STARTING THIS HERE> # include links to help docs / tutorials / wiki instructions also!!

MAVLink autopilot (normal operations):
> mode AUTO
> arm throttle
> wp load "name_of_file_with_waypoints.txt"

Example waypoint files are listed under: ~/ardupilot/Tools/autotest/ArudPlane-Missions/
--> the ones we normally use are formatted like "CMAC-toff-loop.txt"
--> these are in lat-long-alt coordinates (with some additional information)
--> common writeout is as follows:
    # as [long,lat,alt]: (with set orientation)
    waypts = [[-35.362938, 149.165085, 584.409973], [-35.361164, 149.163986, 28.110001], [-35.359467, 149.161697, 99.800003]]
    opened_file.open(filename, 'w')
    opened_file.write("QGC WPL 110")
    firstwaypt = 0; counter = 0
    for pt in waypts:
        [longitude,latitude,altitude] = pt
        if firstwaypt == 0:                       # with constant unchanging orientation
            opened_file.write("%d    1   0   22  15.000000   0.000000    0.000000    0.000000    %d  %d  %d  1\n" % (counter, longitude, latitude, altitude))
            firstwaypt = 1
        else:                                # with constant unchanging orientation
            opened_file.write("%d    0   3   22  15.000000   0.000000    0.000000    0.000000    %d  %d  %d  1\n" % (counter, longitude, latitude, altitude))
        counter += 1
    opened_file.close()

alternately, at the command line (in three separate terminals):
1$ cd catkin_ws; source devel/setup.bash; rosservice ??? "???basic_mode: '', custom_mode: 'AUTO' "???
2$ cd catkin_ws; source devel/setup.bash; rosservice ??? arm ??? "???throttle???: true"???
3$ cd catkin_ws; source devel/setup.bash; rosrun mavros mavwp load "name_of_file_with_waypoints.txt"

Now, with this, you just need to run:
$ cd catkin_ws; source devel/setup.bash; rosrun soi_waypoint_work waypoint_node.py
...and it will listen on a ROS topic (channel) called "/UAV1/waypoint_list" for waypoints of type ???.

You can -test- this ROS node/script at the commadline quickly via a rostopic call:
#string: $ cd catkin_ws; source devel/setup.bash; rostopic pub -1 /UAV1/teststring ???std_msgs/String??? ???"data: 'blah BLAH blah'"???
$ cd catkin_ws; source devel/setup.bash; rostopic pub -1 /UAV1/waypoint_list ???geometry_msgs/Path??? "???: x: ? y:? z:?"???

"""

class StringData(object):
    def __init__(self):
        self.mystring = None #"" # unpacked
        self.mystring_ros = String() # raw format
        self.lock = threading.Lock()

    def callback(self, data):
        self.lock.acquire()
        try: # this looks different depending on the datatype
            self.mystring = data.data
            self.mystring_ros = data
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
            thedata = self.mystring
            self.mystring = None
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
            thedata = self.mystring_ros
            self.mystring_ros = String()
        finally:
            self.lock.release()
        return thedata
            
def waypoint_node():

    rospy.init_node('waypoint_node', anonymous=True)
    string_in = StringData()
    #waypoints_in = WaypointData()
    rospy.Subscriber("/UAV1/teststring", String, string_in.callback)
    #rospy.Subscriber("/UAV1/waypoint_list", soi_waypoint_work/LatLongWayptList, waypoints_in.callback)

    print("Waiting for incoming ROS topic data...")

    while (1):
        hold = string_in.received_data()
        if hold is None:
            pass
        else: # we have new data
            print("String received: %r" % hold)
        #hold2 = waypoints_in.received_data()
        #if hold2.data is None:
        #    pass
        #else: # we have new data
        #    print("Data2 received: %r" % hold2)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
  
    try:
        waypoint_node()
    #except rospy.shutdown(): #ROSError??? etc.:
    #    sys.exit()
    except:
        pass

    sys.exit(0)

# read from the subscribed topic
   
"""  
  def do_load(args):
      wps = []
      wps_file = get_wp_file_io(args)
      with args.file:
          wps = [w for w in wps_file.read(args.file)]
  
      def _load_call(waypoint_list):
          try:
              ret = M.push(waypoints=waypoint_list)
          except rospy.ServiceException as ex:
              fault(ex)
  
          if not ret.success:
              fault("Request failed. Check mavros logs")
  
  print_if(args.verbose, "Waypoints transfered:", ret.wp_transfered)

  def get_wp_file_io(args):
  return M.QGroundControlWP()

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
          _load_call(wps)
      else:
          # Note: _load_call() emit publish on this topic, so callback only changes
          # waypoint 0, and signal done event.
          sub = M.subscribe_waypoints(_fix_wp0)
          if not done_evt.wait(30.0):
              fault("Something went wrong. Topic timed out.")
          else:
              sub.unregister()
  _load_call(wps)
"""
