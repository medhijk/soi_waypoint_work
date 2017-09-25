#include "ros/ros.h"
#include "std_msgs/String.h"
void waytorunCallback(const std_msgs::String::ConstPtr& msg)
{
  ROS_INFO("heard: [%s]", msg->data.c_str());
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "waypoint_node");

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("waytorun", 1000, waytorunCallback);

  ros::spin();

  return 0;
}
