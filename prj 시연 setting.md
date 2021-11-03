1. 웹서버 세팅
    + ROS 관련 세팅
    + ip 관련 세팅
2. 터틀봇 세팅
    + ROS 통신 세팅
    + ROS 로봇 패키지 실행
    + 카메라 송신 모듈 실행
3. 프록시 세팅
    + ROS 통신 세팅
    + ROS 패키지 실행

---

# 1. 웹서버 세팅

## ROS 관련 세팅

`/WAS/Theme/static/ros/dev/ros.js` 에서 다음 부분을 수정한다.

```
ros.connect('ws://localhost:9090');
```

`localhost` 부분을 프록시 서버의 address로 변경

> WAS와 proxy 간 소켓 통신으로 웹 이벤트를 통해 ROS 메세지를 터틀봇까지 전달

## ip 관련 세팅

`WAS/WEB/view/server.py`에서 **ip** 관련 부분.

**ubuntu** 환경에서는 `'ipconfig'` 부분에서 에러가 발생하기 때문에 기존 방식 사용

**windown** 환경에서는 새로 추가된 `def ip()` 사용

`class View:` 내부의 **ip**를 **ip()** 로 변경하며 사용.

---

# 2. 터틀봇 세팅

## ROS 통신 세팅

실행 전 프록시에서 `roscore`가 실행이 되어야한다.

`gedit .bashrc`로 **ROS 통신**에 필요한 **ip** 부분을 수정한다.

```
# Set Ros Network
export ROS_HOSTNAME={{터틀봇의 ip}}
export ROS_MASTER_URI=http://{{프록시의 ip}}:11311
```

## ROS 로봇 패키지 실행

이후 다음을 실행하여 터틀봇에서의 ROS 사용 준비를 완료한다.

`roslaunch turtlebot3_bringup turtlebot3_robot.launch`

**calibration end** 메세지가 확인이 되면 정상적으로 터틀봇 ROS 사용이 준비가 된 것.

## 카메라 송신 모듈 실행

```
cd workspace && source cv_socket/bin/activate
cd cam_server
python SERVER2.py
```

실행에 앞서서 `SERVER2.py` 코드 수정 필요

`def main()` 의 `TCP_IP`를 **웹서버 ip**로 수정

---

# 3. 프록시 세팅

## ROS 통신 세팅

실행 전 프록시에서 `roscore`가 실행이 되어야한다.

`gedit .bashrc`로 **ROS 통신**에 필요한 **ip** 부분을 수정한다.

```
# Set Ros Network
export ROS_HOSTNAME={{프록시의 ip}}
export ROS_MASTER_URI=http://{{프록시의 ip}}:11311
```

## ROS 패키지 실행

**ros master 실행**

`roscore`

**ros socket 실행**

`roslaunch rosbridge_server rosbridge_websocket.launch address:={프록시의 ip}`

**robot pose publisher (좌표 변환기) 실행**

`cw` 후 `source devel/setup.bash`

`rosrun robot_pose_publisher robot_pose_publisher`

**Navigation 실행**

`tw` 후 `source devel/setup.bash`

`roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml`



### 시뮬레이션 환경일 때는

**gazebo (시뮬레이션) 실행**

`cw` 후 `source devel/setup.bash`

`roslaunch turtlebot3_gazebo turtlebot3_world.launch`



### SLAM 지도 저장하는 법

**SLAM 실행**

`tw` 후 `source devel/setup.bash`

`roslaunch turtlebot3_slam turtlebot3_slam.launch slam_method:=gmapping`

**컨트롤러 실행**

`roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch`

**지도 완성 후 저장**

`rosrun map_server map_saver -f ~/map`

---

자율주행 기능을 웹으로 사용할 때

- **클릭**은 목표지점 명령

- **더블클릭**은 초기위치 설정 명령

초기위치 설정은 처음에만 하면되기 때문에 더블클릭하지 않도록 조심한다.