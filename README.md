# soi_waypoint_work

#######################################################################################################################################
#Initial set up (follow this only after you have ardupilot installed. Instructions for setting up ardupilot with ROS can be found here
######################################################################################################################################
    $ cd catkin_ws/src
    $ git clone https://github.com/medhijk/soi_waypoint_work.git
    $ cd ..
    $ catkin_make
    $ cd src/soi_wapoint_work/scripts
    $ cp copytextfile.py /$HOME/ardupilot/Tools/autotest/ArduPlane-Missions
#################################################################################
#################################################################################

First, run roscore in a new terminal
    $ roscore

Second, in a new terminal, run subscriber node
    $ cd $HOME/catkin_ws/src/soi_waypoint_work/launch
    $ chmod +x first-script.sh
    $ ./first-script.sh

Third, give Test command to be sent for publishing waypoint msg
    $ rostopic pub -l /UAV1/waypoint_list mavros_msgs/WaypointList '[{frame: 3, command: 16, is_current: 0, autocontinue: 1,param2: 1,param3: 0, param4: 0, x_lat: -35.359467, y_long: 149.161697, z_alt: 99.800003}]'

###### You can close roscore now as well as the test command and first-script.sh########

Fourth, Run the autopilot & mavros in a new terminal
    $ cd $HOME/catkin_ws/src/soi_waypoint_work/launch
    $ chmod +x daily-script.sh
    $ ./daily-script.sh

Fifth, Run the command script for autopilot after mavros has loaded
    $ cd $HOME/catkin_ws/src/soi_waypoint_work/launch
    $ chmod +x command.sh
    $ ./command.sh


###### That's it!!!! The plane should follow the waypoint now!!!! #######
