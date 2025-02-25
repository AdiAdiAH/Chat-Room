import socket
import select
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
address = ("127.0.0.1", 0)
try:
    sock.bind(address)
except Exception as e:
    print("Issue connecting; Check")
    print(e)
    pass
sock.connect(("127.0.0.1", 10000))
try:
    while True:
        message = input("Send Message\n")
        if message.lower().strip() == "close":
            break
        print(f"sending {message}")
        sock.sendall(message.encode('utf-8'))
        amount_received = 0
        amount_expected = len(message)
        
        while amount_received < amount_expected:
            data = sock.recv(1024)
            amount_received += len(data)
            print(f"received {data}")
            
            
finally:
    print("closing socket")
    sock.close()