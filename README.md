# Romi Control
An alternative control mechanism for driving the Romi (WPI RBE 1001, 2020).

#### Warning
The Romi appears to randomly disconnect when the batteries are getting low. If this happens 
multiple times, try replacing the batteries as a first debugging step.

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

## Controller Buttons
The left and right joysticks correspond to forwards-backwards and left-right, accordingly.
The left and right triggers correspond to raising and lowering the lifting arm.

## Usage
1. Connect to the Romi WiFi network (instructions can be found [here](https://github.com/WPIRoboticsEngineering/RBE1001Lib#ap-mode-in-lab-use)).
2. Connect a controller via bluetooth (or USB, see above).
3. Run `src/romi.py`

## Speed Control
The speed of the Romi is somewhat slow with the existing RCCTL file. There is a replacement file
in `arduino/RCCTL.ino`. This file is very similar with two relevant additions. On lines 13-14 you
can apply a modifier to the speed and turning rate of the robot:

```cpp
float MOTOR_SPEED_MULTIPLIER = 3;
float MOTOR_TURN_MULTIPLIER = 0.6;
```

