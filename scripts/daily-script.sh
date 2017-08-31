#!/bin/bash

#cd $HOME
#xterm -hold -e "roscore" &


# we may need to tell the waypoint_node file that it is executable
#cd $HOME/catkin_ws/src/soi_waypoint_work/scripts
#xterm -hold -e "chmod +x waypoint_node.py" &


# running the waypoint_node which listens to the topic /UAV1/waypoint_list
#cd $HOME/catkin_ws/src/soi_waypoint_work/scripts
#xterm -hold -e "python waypoint_node.py" &

# don't run further until topic is subscribed

# writing waypoints received to a text file
#cd $HOME/ardupilot/Tools/autotest/ArduPlane-Missions
#xterm -hold -e "rostopic echo -p /UAV1/waypoint_list > hst.txt" &


# some translation might be required here to copy the rostopic data in hst.txt to the correct format for ardupilot to read from


# adding directories to the search path
#cd $HOME
#xterm -hold -e "export PATH=$PATH:$HOME/jsbsim/src; export PATH=$PATH:$HOME/ardupilot/Tools/autotest; export PATH=/usr/lib/ccache:$PATH; . ~/.bashrc" &

# copying ROS topic_info into proper WaypointList format
cd $HOME/ardupilot/Tools/autotest/ArduPlane-Missions
xterm -hold -e "python copytextfile.py" &

# launching ardupilot with SITL
cd $HOME/ardupilot/ArduPlane
xterm -hold -e "sleep 3; sim_vehicle.py --console --map --aircraft test" &


# launching mavros
cd $HOME/ardupilot/launch
xterm -hold -e "sleep 20; roslaunch apm.launch" &

## loading waypoints through ros service
#cd $HOME/ardupilot/Tools/autotest/ArduPlane-Missions
#xterm -hold -e "sleep 35; rosrun mavros mavwp load hst.txt" &


## changing the mode in ardupilot through ros service
#xterm -hold -e "sleep 35; rosrun mavros mavsys mode -c auto" &


## changing the arming status through ros service
#xterm -hold -e "sleep 35; rosrun mavros mavsafety arm"


exit 0
