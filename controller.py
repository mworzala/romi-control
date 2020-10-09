from enum import Enum
import glfw
import math

CALIBRATION_TOLERANCE = 0.1

class SteeringType(Enum):
    TANK = 2
    CAR  = 0

class Button(Enum):
    A = 0
    B = 1
    X = 3
    Y = 4
    LEFT_BUMPER = 6
    RIGHT_BUMPER = 7
    LEFT_THUMB = 13
    RIGHT_THUMB = 14
    DPAD_UP = 17
    DPAD_RIGHT = 18
    DPAD_DOWN = 19
    DPAD_LEFT = 20

class Controller:
    """
    Represents a controller capable of controlling the Romi.

    Anything with the relevant buttons which is detected by 
    GLFW should work fine, but only the following are explicitly
    supported and tested:
      - XBox One Controller
    """

    last_stick = (0.0, 0.0)
    stick = (0.0, 0.0)

    last_trigger = (0.0, 0.0)
    trigger = (0.0, 0.0)

    buttons = []

    def __init__(self):
        if not glfw.init():
            raise RuntimeError('Failed to initialize GLFW!')

    def find_joystick(self, printName = True):
        if not glfw.joystick_present(glfw.JOYSTICK_1):
            raise LookupError('Cannot find controller! Please connect one and ensure it is recognised in slot 0')
        if printName:
            print('Controller:', self.get_joystick_name())

    def get_joystick_name(self):
        return glfw.get_joystick_name(glfw.JOYSTICK_1).decode()

    def get_joystick_pos_polar(self):
        (x, y) = self.stick

        # Zero x and y if small to account for controller mis-calibration
        if x < CALIBRATION_TOLERANCE and x > -CALIBRATION_TOLERANCE:
            x = 0
        if y < CALIBRATION_TOLERANCE and y > -CALIBRATION_TOLERANCE:
            y = 0
        
        # Convert to polar
        theta = math.atan2(y, x)
        mag   = min(math.sqrt(x*x + y*y), 1.0)

        # Check if these are new values
        changed = self.last_stick != self.stick
        return changed, theta, mag
    
    def get_trigger_pos(self):
        (lt, rt) = self.trigger

        # Check if these are new values
        changed = self.last_trigger != self.trigger
        return changed, lt, rt
    
    def is_button_pressed(self, button):
        # Buttons are not initialized or invalid button
        if button.value >= len(self.buttons) or button.value < 0:
            return False
        return self.buttons[button.value] == 1
    
    def update_inputs(self, steering_type = SteeringType.TANK):
        # TODO docstring

        # Update GLFW input
        glfw.poll_events()

        # Read the C array of axes and transform to a list
        (axes_ptr, axis_count) = glfw.get_joystick_axes(glfw.JOYSTICK_1)
        axes = [axes_ptr[i] for i in range(axis_count)]

        # Update last and current x/y depending on steering type
        self.last_stick = self.stick
        self.stick = (-axes[steering_type.value], 
                      -axes[1])
        
        # Update last and current trigger values
        self.last_trigger = self.trigger
        self.trigger = ((axes[5] + 1) / 2, (axes[4] + 1) / 2)

        # Get buttons
        (btns_ptr, btn_count) = glfw.get_joystick_buttons(glfw.JOYSTICK_1)
        self.buttons = [btns_ptr[i] for i in range(btn_count)]
    