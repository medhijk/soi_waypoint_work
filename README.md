# soi_waypoint_work
NOTE: This is currently a work in development. At present, the arduplane is set up to follow only a first set of waypoints in a mission.

TODO:
* cleanly handle multiple sets of waypoints received (second set, third set, fourth set, ...)
* streamlining of code

This package has been tested to work under Ubuntu 14.04.

Initial set up (follow this only after you have ardupilot installed. Instructions for setting up ardupilot with ROS can be found here: https://github.com/AS4SR/general_info/wiki/ArduPilot:-Instructions-to-set-up-and-run-an-autopilot-using-SITL-and-Gazebo-simulator 

```
$ cd catkin_ws/src
$ git clone https://github.com/medhijk/soi_waypoint_work.git>
$ cd ..
$ catkin_make
$ source devel/setup.bash
```

First, run roscore in a new terminal
```
$ roscore
```

Second, run the autopilot & mavros in a new terminal.
If you have not added these lines to the end of your ”.bashrc” in the home directory during ardupilot installation, export these paths once now:
```
cd $HOME
export PATH=$PATH:$HOME/jsbsim/src
export PATH=$PATH:$HOME/ardupilot/Tools/autotest
export PATH=/usr/lib/ccache:$PATH
. ~/.bashrc
```
Run the autopilot
```
$ cd catkin_ws
$ source devel/setup.bash
$ cd src/soi_waypoint_work/scripts
$ chmod +x daily-script.sh
$ ./daily-script.sh
```

Third, in a new terminal, run subscriber node
```
$ cd catkin_ws
$ source devel/setup.bash
$ cd src/soi_waypoint_work/scripts
$ python waypoint_node_new.py
```

Fourth, give Test command to be sent for publishing waypoint msg
```
rostopic pub -l /UAV1/testGeoPoint soi_waypoint_work/LatLongWayptList "geopoints:
- latitude: 149.161697
  longitude: -35.359467
  altitude: 99.800003"
```
###### That's it!!!! The plane should follow the waypoint now!!!! ######
