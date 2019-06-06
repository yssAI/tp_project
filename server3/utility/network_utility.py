import socket
import psutil
from random import randint
import port_for


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def get_free_port_with_range(low, high):

    import port_for
    port_for.select_random(ports=set(range(low, high)))
    port = low  # First port.
    while low <= port <= high:  # Port high is last port you can access.
        try:
            try:
                s = socket.socket(socket.AF_INET,
                                       socket.SOCK_STREAM, 0)  # Create a
                # socket.
            except:
                print("Error: Can't open socket!\n")
                break  # If can't open socket, exit the loop.
            s.connect(("127.0.0.1", port))
            # Try connect the port. If port is not listening, throws ConnectionRefusedError.
            connected = True
        except ConnectionRefusedError:
            connected = False
        finally:
            if connected and port != s.getsockname()[1]:  # If connected,
                print("{}:{} Open \n".format("127.0.0.1", port))  # print port.
                return port
            port = port + 1  # Increase port.
            s.close()  # Close socket.
    raise Exception('no port available')
