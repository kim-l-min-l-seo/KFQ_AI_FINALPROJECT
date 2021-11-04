# 프록시에서 실행시킬 것

**ros master 실행**

roscore

**ros socket 실행**

roslaunch rosbridge_server rosbridge_websocket.launch address:=`여기다가 중계컴 ip입력`

**robot pose publisher (좌표 변환기) 실행**

`cw` 후 `source devel/setup.bash`

rosrun robot_pose_publisher robot_pose_publisher

**Navigation 실행**

`tw` 후 `source devel/setup.bash`

roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml




## 시뮬레이션 환경일 때는

**gazebo (시뮬레이션) 실행**

`cw` 후 `source devel/setup.bash`

roslaunch turtlebot3_gazebo turtlebot3_world.launch



## SLAM 지도 저장하는 법

**SLAM 실행**

`tw` 후 `source devel/setup.bash`

roslaunch turtlebot3_slam turtlebot3_slam.launch slam_method:=gmapping

**컨트롤러 실행**

roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch

**지도 완성 후 저장**

rosrun map_server map_saver -f ~/map



# 터틀봇에서 실행시킬 것

**로봇 실행**

roslaunch turtlebot3_bringup turtlebot3_robot.launch
