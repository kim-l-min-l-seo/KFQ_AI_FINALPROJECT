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
    width : 300,
    height : 300
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
    console.log(cmd_vel_listener.name + 'linear x: ' + cmd_vel.linear.x);
    // console.log(cmd_vel_listener.name + 'linear y: ' + cmd_vel.linear.y);
    // console.log(cmd_vel_listener.name + 'linear z: ' + cmd_vel.linear.z);
    // console.log(cmd_vel_listener.name + 'angular x: ' + cmd_vel.angular.x);
    // console.log(cmd_vel_listener.name + 'angular y: ' + cmd_vel.angular.y);
    // console.log(cmd_vel_listener.name + 'angular z: ' + cmd_vel.angular.z);
    // console.log(cmd_vel);
    var vel = document.getElementById('vel');
    vel.innerText = cmd_vel.linear.x;
  });

  // imu
  var imu_listener = new ROSLIB.Topic({
    ros : ros,
    name : '/imu',
    messageType : 'sensor_msgs/Imu'
  });
  // Then we add a callback to be called every time a message is published on this topic.
  imu_listener.subscribe(function(imu) {
    // console.dir(imu);
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

  //
  //
  var txt_listener = new ROSLIB.Topic({
    ros : ros,
    name : '/txt_msg',
    messageType : 'std_msgs/String'
  });

  txt_listener.subscribe(function(m) {
    document.getElementById("msg").innerHTML = m.data;
  });

  move = function (linear, angular) {
    var twist = new ROSLIB.Message({
      linear: {
        x: linear,
        y: 0,
        z: 0
      },
      angular: {
        x: 0,
        y: 0,
        z: angular
      }
    });
    cmd_vel_listener.publish(twist);
  }

  // 
  txt_listener.subscribe(function(m) {
    document.getElementById("msg").innerHTML = m.data;
    move(1, 0);
  });

  //
  createJoystick = function () {
    var options = {
      zone: document.getElementById('zone_joystick'),
      threshold: 0.1,
      position: { left: 50 + '%' },
      mode: 'static',
      size: 150,
      color: '#000000',
    };
    manager = nipplejs.create(options);

    linear_speed = 0;
    angular_speed = 0;

    self.manager.on('start', function (event, nipple) {
      console.log("Movement start");
      timer = setInterval(function () {
        move(linear_speed, angular_speed);
      }, 25);
    });

    self.manager.on('move', function (event, nipple) {
      console.log("Moving");
      max_linear = 5.0; // m/s
      max_angular = 2.0; // rad/s
      max_distance = 75.0; // pixels;
      linear_speed = Math.sin(nipple.angle.radian) * max_linear * nipple.distance/max_distance;
      angular_speed = -Math.cos(nipple.angle.radian) * max_angular * nipple.distance/max_distance;
    });

    self.manager.on('end', function () {
      console.log("Movement end");
      if (timer) {
        clearInterval(timer);
      }
      self.move(0, 0);
    });
  }
  window.onload = function () {
    createJoystick();
  }
}