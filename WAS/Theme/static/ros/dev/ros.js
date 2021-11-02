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
  ros.connect('ws://localhost:9090');

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
  
  // clock
  var clock_listener = new ROSLIB.Topic({
    ros : ros,
    name : '/clock',
    messageType : 'rosgraph_msgs/Clock'
  });
  // Then we add a callback to be called every time a message is published on this topic.
  clock_listener.subscribe(function(clock) {
    // console.log(clock.clock);
    // console.log(clock.clock.secs);
    // console.log(clock.clock.nsecs);
    // console.log(clock);
  });

  // cmd_vel
  var cmd_vel_listener = new ROSLIB.Topic({
    ros : ros,
    name : '/cmd_vel',
    messageType : 'geometry_msgs/Twist'
  });
  // Then we add a callback to be called every time a message is published on this topic.
  cmd_vel_listener.subscribe(function(cmd_vel) {
    var vel_x = document.getElementById('vel_linear_x');
    vel_x.innerText = cmd_vel.linear.x;
    var vel_z = document.getElementById('vel_angular_z');
    vel_z.innerText = cmd_vel.angular.z;
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
    imu_orientation_w.innerText = 'w: '+imu.orientation.w;
    var imu_orientation_x = document.getElementById('imu_orientation_x');
    imu_orientation_x.innerText = 'x: '+imu.orientation.x;
    var imu_orientation_y = document.getElementById('imu_orientation_y');
    imu_orientation_y.innerText = 'y: '+imu.orientation.y;
    var imu_orientation_z = document.getElementById('imu_orientation_z');
    imu_orientation_z.innerText = 'z: '+imu.orientation.z;
    var imu_angular_velocity_x = document.getElementById('imu_angular_velocity_x');
    imu_angular_velocity_x.innerText = 'x: '+imu.angular_velocity.x;
    var imu_angular_velocity_y = document.getElementById('imu_angular_velocity_y');
    imu_angular_velocity_y.innerText = 'y: '+imu.angular_velocity.y;
    var imu_angular_velocity_z = document.getElementById('imu_angular_velocity_z');
    imu_angular_velocity_z.innerText = 'z: '+imu.angular_velocity.z;
    var imu_linear_acceleration_x = document.getElementById('imu_linear_acceleration_x');
    imu_linear_acceleration_x.innerText = 'x: '+imu.linear_acceleration.x;
    var imu_linear_acceleration_y = document.getElementById('imu_linear_acceleration_y');
    imu_linear_acceleration_y.innerText = 'y: '+imu.linear_acceleration.y;
    var imu_linear_acceleration_z = document.getElementById('imu_linear_acceleration_z');
    imu_linear_acceleration_z.innerText = 'z: '+imu.linear_acceleration.z;
  });

  // // battery state
  // var battery_state_listener = new ROSLIB.Topic({
  //   ros : ros,
  //   name : '/battery_idk',
  //   messageType : 'sensor_msgs/BatteryState Message'
  // });
  // // Then we add a callback to be called every time a message is published on this topic.
  // battery_state_listener.subscribe(function(battery) {
  //   console.log(battery.perentage);
  //   // console.log(status);
  // });

  // cmd_vel
  var nav_status = new ROSLIB.Topic({
    ros : ros,
    name : '/move_base/status',
    messageType : 'actionlib_msgs/GoalStatusArray'
  });
  // Then we add a callback to be called every time a message is published on this topic.
  nav_status.subscribe(function(status) {
    var length = status.status_list.length;
    if (length == 1){
      var nav_status = document.getElementById('nav_status');
      nav_status.innerText = status.status_list[0].text;
      // console.log(status.status_list[0]);
    }
    else {
      var nav_status = document.getElementById('nav_status');
      nav_status.innerText = status.status_list[1].text;
      // console.log(status.status_list[1]);
    }
  });
}