function init() {
  // Connecting to ROS
  // -----------------
  var ros = new ROSLIB.Ros();

  // If there is an error on the backend, an 'error' emit will be emitted.
  ros.on('error', function(error) {
    document.getElementById('connecting').style.display = 'none';
    document.getElementById('connected').style.display = 'none';
    document.getElementById('closed').style.display = 'none';
    document.getElementById('error').style.display = 'inline';
    console.log(error);
  });

  // Find out exactly when we made a connection.
  ros.on('connection', function() {
    console.log('Connection made!');
    document.getElementById('connecting').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('closed').style.display = 'none';
    document.getElementById('connected').style.display = 'inline';
  });

  ros.on('close', function() {
    console.log('Connection closed.');
    document.getElementById('connecting').style.display = 'none';
    document.getElementById('connected').style.display = 'none';
    document.getElementById('closed').style.display = 'inline';
  });

  // Create a connection to the rosbridge WebSocket server.
  ros.connect('ws://192.168.0.41:9090');
  // ros.connect('ws://localhost:9090');

  cmd_vel_listener = new ROSLIB.Topic({
    ros : ros,
    name : "/cmd_vel",
    messageType : 'geometry_msgs/Twist'
  });
  var twist = new ROSLIB.Message({
    linear: {
      x: 0,
      y: 0,
      z: 0
    },
    angular: {
      x: 0,
      y: 0,
      z: 0
    }
  });
  cmd_vel_listener.publish(twist);

  // Initialize the teleop.
  var teleop = new KEYBOARDTELEOP.Teleop({
    ros : ros,
    topic : '/cmd_vel'
  });
  teleop.scale = (1);

  // Create the main viewer.
  var viewer = new ROS2D.Viewer({
    divID : 'map',
    width : 516,
    height : 516
  });

  var nav = NAV2D.OccupancyGridClientNav({
    ros : ros,
    rootObject : viewer.scene,
    viewer : viewer
  });
    //Subscribing to a Topic
  //----------------------

  // cmd_vel
  var cmd_vel_listener = new ROSLIB.Topic({
    ros : ros,
    name : '/cmd_vel',
    messageType : 'geometry_msgs/Twist'
  });
  // Then we add a callback to be called every time a message is published on this topic.
  cmd_vel_listener.subscribe(function(cmd_vel) {
    var vel_x = document.getElementById('vel_linear_x');
    vel_x.innerText = '전/후 속도 \u00A0'+cmd_vel.linear.x.toPrecision(10);
    var vel_z = document.getElementById('vel_angular_z');
    vel_z.innerText = '좌/우 속도 \u00A0'+cmd_vel.angular.z.toPrecision(10);
    var vel_x_state = document.getElementById('vel_linear_state');
    var vel_z_state = document.getElementById('vel_angular_state');
    if (cmd_vel.linear.x > 0) {
      vel_x_state.innerText = '전진';
    }
    else if (cmd_vel.linear.x < 0) {
      vel_x_state.innerText = '후진';
    }
    else {
      vel_x_state.innerText = '전/후 모터 정지';
    }

    if (cmd_vel.angular.z > 0) {
      vel_z_state.innerText = '좌회전';
    }
    else if (cmd_vel.angular.z < 0) {
      vel_z_state.innerText = '우회전';
    }
    else {
      vel_z_state.innerText = '좌/우 모터 정지';
    }
  });

  // imu
  var imu_listener = new ROSLIB.Topic({
    ros : ros,
    name : '/imu',
    messageType : 'sensor_msgs/Imu'
  });
  // // Then we add a callback to be called every time a message is published on this topic.
  imu_listener.subscribe(function(imu) {
    var imu_orientation_w = document.getElementById('imu_orientation_w');
    imu_orientation_w.innerText = '지자계 w : \u00A0'+imu.orientation.w;
    var imu_orientation_x = document.getElementById('imu_orientation_x');
    imu_orientation_x.innerText = '지자계 x : \u00A0'+imu.orientation.x;
    var imu_orientation_y = document.getElementById('imu_orientation_y');
    imu_orientation_y.innerText = '지자계 y : \u00A0'+imu.orientation.y;
    var imu_orientation_z = document.getElementById('imu_orientation_z');
    imu_orientation_z.innerText = '지자계 z : \u00A0'+imu.orientation.z;
    var imu_angular_velocity_x = document.getElementById('imu_angular_velocity_x');
    imu_angular_velocity_x.innerText = '각속도 x : \u00A0'+imu.angular_velocity.x;
    var imu_angular_velocity_y = document.getElementById('imu_angular_velocity_y');
    imu_angular_velocity_y.innerText = '각속도 y : \u00A0'+imu.angular_velocity.y;
    var imu_angular_velocity_z = document.getElementById('imu_angular_velocity_z');
    imu_angular_velocity_z.innerText = '각속도 z : \u00A0'+imu.angular_velocity.z;
    var imu_linear_acceleration_x = document.getElementById('imu_linear_acceleration_x');
    imu_linear_acceleration_x.innerText = '가속도 x : \u00A0'+imu.linear_acceleration.x;
    var imu_linear_acceleration_y = document.getElementById('imu_linear_acceleration_y');
    imu_linear_acceleration_y.innerText = '가속도 y : \u00A0'+imu.linear_acceleration.y;
    var imu_linear_acceleration_z = document.getElementById('imu_linear_acceleration_z');
    imu_linear_acceleration_z.innerText = '가속도 z : \u00A0'+imu.linear_acceleration.z;
  });

  // battery state
  var battery_state_listener = new ROSLIB.Topic({
    ros : ros,
    name : '/diagnostics',
    messageType : 'diagnostic_msgs/DiagnosticArray'
  });
  // Then we add a callback to be called every time a message is published on this topic.
  battery_state_listener.subscribe(function(battery) {
    var hardware_id = document.getElementById('power_sys_id');
    var message = document.getElementById('power_sys_msg');
    var name = document.getElementById('power_sys_name');
    hardware_id.innerText = '\u00A0\u00A0연결 : ' + battery.status[3].hardware_id;
    message.innerText = '\u00A0\u00A0상태 : ' + battery.status[3].message;
    name.innerText = battery.status[3].name;
  });
  
  // // battery state
  // var battery_state_listener = new ROSLIB.Topic({
  //   ros : ros,
  //   name : '/battery_state',
  //   messageType : 'sensor_msgs/BatteryState'
  // });
  // // Then we add a callback to be called every time a message is published on this topic.
  // battery_state_listener.subscribe(function(battery) {
  //   var battery_percentage = document.getElementById('battery_percentage');
  //   battery_percentage.innerText = battery.percentage;
  // });

  // nav status
  
  var nav_status = new ROSLIB.Topic({
    ros : ros,
    name : '/move_base/status',
    messageType : 'actionlib_msgs/GoalStatusArray'
  });
  // Then we add a callback to be called every time a message is published on this topic.
  nav_status.subscribe(function(status) {
    var length = status.status_list.length;
    
    if (length == 1) {
      // var nav_status = document.getElementById('nav_status');
      if (status.status_list[0].text == "Goal reached.") {
        var nav_status = document.getElementById('nav_status');
        nav_status.innerText =  '목표 지점 도착 완료';
      }
      else if (status.status_list[0].text == "This goal has been accepted by the simple action server") {
        var nav_status = document.getElementById('nav_status');
        nav_status.innerText = '목표 지점 전달 중';
      }
      else {
        var nav_status = document.getElementById('nav_status');
        nav_status.innerText = '명령 전달 진행 중';
      }
    }
    else {
      if (status.status_list[1].text == "Goal reached.") {
        var nav_status = document.getElementById('nav_status');
        nav_status.innerText =  '목표 지점 도착 완료';
      }
      else if (status.status_list[1].text == "This goal has been accepted by the simple action server") {
        var nav_status = document.getElementById('nav_status');
        nav_status.innerText = '목표 지점 전달 중';
      }
      else {
        nav_status.innerText = '명령 전달 진행 중';
      }
    }
  });
}