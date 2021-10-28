var KEYBOARDTELEOP = KEYBOARDTELEOP || {
    REVISION: "0.3.0"
};
KEYBOARDTELEOP.Teleop = function (a) {
    var b = this;
    a = a || {};
    var c = a.ros,
        d = a.topic || "/cmd_vel",
        e = a.throttle || 1;
    this.scale = 1;
    var f = 0,
        h = 0,
        i = new ROSLIB.Topic({ros: c, name: d, messageType: "geometry_msgs/Twist"}),
        max_lin_vel = 0.22,
        max_ang_vel = 2.84,
        j = function (a, c) {
            var d = f,
                k = h,
                l = !0,
                m = 0;
            switch (c === !0 && (m = e * b.scale), a) {
                case 65:
                    if (h < max_ang_vel) {
                        h += .1 * m;
                    }
                    else {
                        h = max_ang_vel;
                    }
                    break;
                case 87:
                    if (f < max_lin_vel) {
                        f += .01 * m;
                    }
                    else {
                        f = max_lin_vel
                    }
                    break;
                case 68:
                    if (h > -max_ang_vel) {
                        h += -.1 * m;
                    }
                    else {
                        h = -max_ang_vel;
                    }
                    break;
                case 83:
                    if (f > -max_lin_vel) {
                        f += -.01 * m;
                    }
                    else {
                        f = -max_lin_vel;
                    }
                    break;
                case 32:
                    h = 0;
                    f = 0;
                default:
                    l = !1
            }
            var n = new ROSLIB.Message({
                angular: {
                    x: 0,
                    y: 0,
                    z: h
                },
                linear: {
                    x: f,
                    y: 0,
                    z: 0
                }
            });
            i.publish(n),
            (d !== f || k !== h) && b.emit("change", n)
        },
        k = document.getElementsByTagName("body")[0];
    k.addEventListener("keydown", function (a) {
        j(a.keyCode, !0)
    }, !1),
    k.addEventListener("keyup", function (a) {
        j(a.keyCode, !1)
    }, !1)
},
KEYBOARDTELEOP.Teleop.prototype.__proto__ = EventEmitter2.prototype;