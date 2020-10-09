from asyncio import get_event_loop, sleep, CancelledError
from websockets import connect
from random import random
from struct import pack

from controller import Controller

LARGE_INT = 2147483000
SLIDER_SPEED = 0.05

class RomiController:
    """
    TODO
    """
    controller = Controller()

    websocket = None
    tasks = []

    # Represents the webpage slider
    # (value, changed)
    slider = (float(0), False)

    def __init__(self):
        self.controller.find_joystick()

    async def connect(self, uri = 'ws://192.168.4.1/test'):
        async with connect(uri) as websocket:
            print('Connected to Romi.')
            self.websocket = websocket

            # Schedule tasks
            self.__schedule(self.send_heartbeat, 1)
            self.__schedule(self.send_value_updates, 0.06)

            # Read messages from romi, and ignore them
            # This loop will terminate on disconnection
            async for _ in websocket:
                pass

            print('Romi disconnected, cleaning up.')
            for task in self.tasks:
                try:
                    task.cancel()
                except CancelledError:
                    pass
            self.websocket = None
            self.tasks = []

    async def send_heartbeat(self):
        random_uuid = int(random() * LARGE_INT) + 1

        packet = [          # Heartbeat Packet
            80,             # ID (0x50)
            random_uuid     # Random Number (never zero)
        ]
        
        await self.__send_packet(packet)

    async def send_value_updates(self):
        self.controller.update_inputs()

        await self.send_joystick_pos()
        await self.send_arm_pos()

    async def send_joystick_pos(self):
        (changed, theta, magnitude) = self.controller.get_joystick_pos_polar()
        # Avoid sending existing values
        if not changed:
            return 

        packet = [          # Joystick Update Packet
            32,             # ID (0x20)
            float(1),       # X Position (Unused)
            float(1),       # Y Position (Unused)
            theta,          # Angle in Radians
            magnitude       # Magnitude (Max 1)
        ]

        await self.__send_packet(packet)

    async def send_arm_pos(self):
        # Update slider value
        (_, lt, rt) = self.controller.get_trigger_pos()
        if lt != 0 or rt != 0:
            self.slider = (
                min(max(self.slider[0] + (lt * -SLIDER_SPEED) + (rt * SLIDER_SPEED), 0.0), 1.0), 
                True
            )
        
        # Avoid sending existing values
        if not self.slider[1]:
            return
        self.slider = (self.slider[0], False)

        packet = [          # Slider Update Packet
            48,             # ID (0x30)
            0,              # Slider ID (Always 0)
            self.slider[0]  # Slider Percentage (Max 1)
        ]

        await self.__send_packet(packet)

    def __schedule(self, task, interval):
        async def __run(_task, _interval):
            while True:
                await _task()
                await sleep(_interval)
        
        handle = get_event_loop().create_task(__run(task, interval))
        self.tasks.append(handle)

    async def __send_packet(self, packet):
        """
        TODO docstring, also packet is a list of ints and/or floats
        """
        buffer = bytearray()
        
        # Write each element of data (and the id) to the buffer
        for elem in packet:
            if type(elem) == int: # TODO probably can use pack here as well
                buffer.extend(elem.to_bytes(4, 'little'))
            elif type(elem) == float:
                buffer.extend(pack('<f', elem))
            else:
                raise RuntimeError('Protocol does not support non-int, non-float data values.')
        
        # Ensure there is an active connection
        if self.websocket is None:
            raise RuntimeError('Cannot send a packet to a disconnected server.')
        # Send the packet
        await self.websocket.send(buffer)
    
if __name__ == '__main__':
    romi = RomiController()

    get_event_loop().run_until_complete(romi.connect())
