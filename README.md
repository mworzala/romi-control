# Romi Control
An alternative control mechanism for driving the Romi (WPI RBE 1001, 2020).

## Protocol
The protocol can be found [natively here](https://github.com/WPIRoboticsEngineering/RBE1001Lib/blob/master/src/WebPage.cpp#L48), or organized in [PROTOCOL.md](https://github.com/mworzala/romi-control/blob/master/PROTOCOL.md).

The entire protocol is not implemented here, only the required pieces for control.

## Controller Support
The only explicit support is Wireless XBox One controllers, however GLFW is
used for controller input.

Whatever the controller, it must have two joystick inputs as well as a left
and right trigger.

Note: As of now, button mapping is not dynamic, so buttons may not make sense
for other controllers.

## Starting
1. Connect to the Romi WiFi network (instructions can be found [here](https://github.com/WPIRoboticsEngineering/RBE1001Lib#ap-mode-in-lab-use)).
2. Connect a controller via bluetooth (or USB, see above).
3. Run `romi.py`