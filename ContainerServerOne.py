import socket

HOST = "127.0.0.1"
PORT = 3000
ACK_COUNTER = 0
GENERATOR = 2

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:     #automatically closes sock at the end of the block
        sock.bind((HOST, PORT))
        sock.listen(5)
        connection, address = sock.accept()
        with connection:                                                #automatically closes connection at the end of the block
            print("Connected to: ", address)
            while True:
                clientMessage = connection.recv(8192)
                if clientMessage:
                    x = int(repr(clientMessage)[2:len(repr(clientMessage)) - 1])
                    x = str(pow(GENERATOR, x))
                    print(repr(clientMessage)[2:len(repr(clientMessage)) - 1], bytes(x, "UTF-8"))
                    ACK_COUNTER += 1
                    connection.sendall(bytes(x, "UTF-8"))
                    connection.sendall(bytes("ACK-" + str(ACK_COUNTER), "UTF-8"))
                else:
                    break
except Exception as exceptions:
    print("Socket was closed due to ", socket.error)