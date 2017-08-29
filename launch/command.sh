#!/bin/bash


# loading waypoints through ros service
cd $HOME/ardupilot/Tools/autotest/ArduPlane-Missions
xterm -hold -e "rosrun mavros mavwp load hst.txt" &


# changing the mode in ardupilot through ros service
xterm -hold -e "sleep 5; rosrun mavros mavsys mode -c auto" &


# changing the arming status through ros service
xterm -hold -e "sleep 3; rosrun mavros mavsafety arm"

exit 0


#or
#load everything in the same terminal
#cd $HOME/ardupilot/Tools/autotest/ArduPlane-Missions
#xterm -hold -e "rosrun mavros mavwp load hst.txt; sleep 5; rosrun mavros mavsys mode -c auto; sleep 3; rosrun mavros mavsafety arm"
