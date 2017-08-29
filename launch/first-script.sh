#!/bin/bash

#cd $HOME
#xterm -hold -e "roscore; sleep 20" &
cd $HOME/catkin_ws
xterm -hold -e "source devel/setup.bash; rosrun soi_waypoint_work waypoint_node.py" &
cd $HOME/ardupilot/Tools/autotest/ArduPlane-Missions
xterm -hold -e "rostopic echo -p /UAV1/waypoint_list > topic_info.txt" &


exit 0
