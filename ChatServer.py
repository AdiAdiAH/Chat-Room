import socket
import select
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(server_sock)
inputs = [server_sock]
outputs = []
try:
    address = ("127.0.0.1", 10000)
    print(address)
    ret = server_sock.bind(address)    
    print(ret)
    ret = server_sock.listen(2)
    print(ret)
    while True:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for s in readable:
            if s is server_sock:
                # The server socket is readable now, i.e., a new connection is received
                client_sock, client_address = server_sock.accept()
                print(f"connection from {client_address}")
                host = client_sock.getpeername()
                client_sock.setblocking(0)
                inputs.append(client_sock)
            else:
                # A socket associated with some connection became readable, i.e.,
                # either some data came or the connection got closed or some other error.
                data = s.recv(1024)
                print(f"{data} from {host}")
                if data:
                    s.send(data)
                else:
                    inputs.remove(s)
                    s.close()
        # We are not checking for writable sockets yet. We are only sending small chunks of data.
        # Hence, every write should work in one shot. We shall check for writability when we start
        # sending big chunks and socket may not accept it in one go.
finally:
    server_sock.close()
    print("Socket has been closed")


