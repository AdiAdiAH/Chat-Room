import socket
import sys
import select
if len(sys.argv) > 1:
    name = sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect(("192.168.56.2", 10000))
    sock.sendall(name.encode('utf-8'))
    print(f"Chat Window is Ready for {name}")
    inputs = [sys.stdin, sock]
    outputs = [sys.stdout, sock]
    errors = [sock]
    while True:
        #print(f"{inputs=}, {outputs=}, {errors=}\n")
        readable, writable, exceptional = select.select(inputs, outputs, errors)
        for s in readable:
            if s is sock:
                data = s.recv(1024)
                if data:
                    print(f"{' '*10}{data.decode()}")
                else:
                    inputs.remove(s)
                    outputs.remove(s)
                    errors.remove(s)
                    print ("The connection is closed")
                    s.close()
            else:
                message = sys.stdin.readline().strip()
                if message:
                    sock.sendall(message.encode('utf-8'))

else:
    print("Please Provide a Username")
