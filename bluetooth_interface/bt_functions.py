import bluetooth
from bluetooth.btcommon import BluetoothError

def search():
    try:
        message = "Searching for nearby BlueTooth devices..."
        print(message)

        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                                                flush_cache=True, lookup_class=False)

        message = f"Found {len(nearby_devices)} devices"
        print(message)

        devices = {}

        for addr, name in nearby_devices:
            devices[name] = addr

        return devices
    except:
        devices = {}
        print('Could not find any devices')
        return devices

def connect(bd_addr, port_num):
    try:
        print(f'Connecting to {bd_addr}')
        sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        print('got sock instance')
        sock.connect((bd_addr, port_num))
        msg = f'Connected to {bd_addr}'
        #msg = sock.recv(1024)
        print('returning sock')
        return (sock, msg)
    except BluetoothError as error:
        print(error)
        msg = 'Failed to connect to device'
        return (1, msg)
    except:
        return (1, 'An error has occured')

def send_serial(sock, message):
    try:
        print('sending message')
        sock.send(message)
        #sock.settimeout(10)
        try:
            msg = sock.recv(1024)
            if len(msg) < 3:
                msg = 'Error with parsing message'
        except socket.error:
            print('connection timed out')
            return 'Connection timed out'
        try:
            decoded_msg = msg.decode('utf-8')
        except:
            return msg
        else:
            msg = decoded_msg
        return msg
    except BluetoothError as error:
        print(error.message)
        return 1
    except:
        return 1

def close_connection(sock):
    try:
        sock.close()
    except:
        return 1
