import zmq
from enum import Enum

class ConnectionMode(Enum):
    publisher = zmq.PUB
    subscriber = zmq.SUB
    request = zmq.REQ
    reply = zmq.REP

class Connector:
    def __init__(self, connection_type, address, port: None, mode: ConnectionMode):
        self.connected = False
        if not connection_type:
            print(f'connection type should be passed to Connector')
            return
        if not mode:
            print(f'mode should be passed to Connector')
            return

        if address:
            self.fullAddress = connection_type + ':///' + address
        else:
            self.fullAddress = connection_type + '///:*'

        if port:
            self.fullAddress += ':'

        print(f'Connector: full address {self.fullAddress}')

        try:
            self.context = zmq.Context()
        except Exception as e:
            print(f"can't take zmq context - exception {e}")

        self.mode = mode

        try:
            self.socket = self.context.socket(mode.value)
        except Exception as e:
            print(f"can't take zmq socket - exception {e}, mode: {mode.name}")

    def connect(self):
        if self.context.closed:
            print(f'context closed trying to recovery')
            self.context = zmq.Context()
        if self.socket.closed:
            print(f'socket closed - trying to recovery')
            self.socket = self.context.socket(self.mode.value)
        try:
            self.socket.connect(self.fullAddress)
        except Exception as e:
            self.connected = False
            print(f"can't connect - exception {e}, full address: {self.fullAddress}, mode {self.mode.name}")
            return
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        print(f'connected to the address {self.fullAddress}')
        self.connected = True

    def block_read_message(self):
        try:
            message = self.socket.recv_string()
            return message
        except Exception as e:
            print(f'filed to read. exception {e}')
            self.connected = False

    def block_send_message(self, message: str):
        try:
            self.socket.send(message)
        except Exception as e:
            print(f'filed to send {e}')
            self.connected = False





