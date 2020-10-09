from time import sleep
from colorama import init as colorama_init, Fore, Back, Style, Cursor
from controller import Controller, Button
from os import get_terminal_size
import re

# 
# START UTILITY FUNCTIONS
#

cols, rows = get_terminal_size()
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def ascii_len(text):
    return len(ansi_escape.sub('', text))

def ascii_ljust(text, size):
    return f'{text}{" " * (size - ascii_len(text))}'

def space_between(left, right):
    return ascii_ljust(f'{left}', cols - ascii_len(right)) + f'{right}'

def print_b(text, end='\n'):
    print(ascii_ljust(f'{text}', cols), end=end)

def bool_symbol(symbol, cond):
    if cond:
        return Fore.GREEN + str(symbol)
    else:
        return Fore.RED + str(symbol)

#
# END UTILITY FUNCTIONS
# 

def main():
    colorama_init()
    c = Controller()
    c.find_joystick(False)

    while True:
        c.update_inputs()
        
        # Start Printout
        print_b(space_between(
            f'{Fore.BLUE}Controller Debug{Fore.CYAN}',
            c.get_joystick_name()
        ), end='\n\n')

        CHECK = Fore.GREEN + str("✓")
        CROSS = Fore.RED + str("✗")

        # Joystick Position
        (js_changed, theta, magnitude) = c.get_joystick_pos_polar()
        print_b(f'{Fore.BLUE}Joystick Position {Fore.LIGHTBLACK_EX}(Polar)')
        print_b(space_between(
            f'{Fore.MAGENTA}θ = {theta:.2f}, |x| = {magnitude:.2f}',
            f'{Fore.LIGHTBLACK_EX}Changed? {CHECK if js_changed else CROSS}'
        ), end='\n\n')

        # Trigger Position
        (trig_changed, lt, rt) = c.get_trigger_pos()
        print_b(f'{Fore.BLUE}Trigger Position {Fore.LIGHTBLACK_EX}(Percent)')
        print_b(space_between(
            f'{Fore.MAGENTA}lt% = {lt:.3f}, rt% = {rt:.3f}',
            f'{Fore.LIGHTBLACK_EX}Changed? {CHECK if trig_changed else CROSS}'
        ), end='\n\n')

        # Buttons
        print_b(f'{Fore.BLUE}Buttons {Fore.LIGHTBLACK_EX}(0 = Up, 1 = Down)')
        print_b(
            bool_symbol('A ', c.is_button_pressed(Button.A)) + 
            bool_symbol('B ', c.is_button_pressed(Button.B)) + 
            bool_symbol('X ', c.is_button_pressed(Button.X)) + 
            bool_symbol('Y ', c.is_button_pressed(Button.Y)) + 
            bool_symbol('↑ ', c.is_button_pressed(Button.DPAD_UP)) + 
            bool_symbol('↓ ', c.is_button_pressed(Button.DPAD_DOWN)) + 
            bool_symbol('← ', c.is_button_pressed(Button.DPAD_LEFT)) + 
            bool_symbol('→ ', c.is_button_pressed(Button.DPAD_RIGHT)) + 
            bool_symbol('LB ', c.is_button_pressed(Button.LEFT_BUMPER)) + 
            bool_symbol('RB ', c.is_button_pressed(Button.RIGHT_BUMPER)) + 
            bool_symbol('LS ', c.is_button_pressed(Button.LEFT_THUMB)) + 
            bool_symbol('RS ', c.is_button_pressed(Button.RIGHT_THUMB))
        )

        # End Printout
        print_b('', end='\r' + Cursor.UP(10))

        sleep(0.06)

if __name__ == '__main__':
    main()
