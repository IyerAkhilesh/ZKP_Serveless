import traceback
import pymysql
import math
import socket
import NumberGenerator_V0 as csprng


HOST = "127.0.0.1"
PORT = 9101
ACK_COUNTER = 0
GENERATOR = 7
power_counter = 12
Nb = math.floor(pow(41, math.e * power_counter / 2)) % 100000000
Nb_factors = csprng.factorizer(Nb)
nb1 = Nb_factors[0: Nb_factors.find(',')]

dbconnection = pymysql.connect(host="localhost", port=3306, user="root", passwd="Akhilesh@1997", db="user_information")
cursor = dbconnection.cursor()

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:     #automatically closes sock at the end of the block
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      #llows the address/port to be reused immediately instead of it being stuck in the TIME_WAIT state for several minutes, waiting for late packets to arrive.
        sock.bind((HOST, PORT))
        sock.listen(0xFF)
        connection, address = sock.accept()
        with connection:                                                #automatically closes connection at the end of the block
            print("Connected to: ", connection, address)
            global public_key, X
            # while True:
            clientMessageOne = connection.recv(8192)
            # if clientMessage:
            X = repr(clientMessageOne)[2:len(repr(clientMessageOne)) - 1]
            print("X", X)
            # print("First", repr(clientMessage)[2:len(repr(clientMessage)) - 1])
            sql = "SELECT public_key FROM credentials where X = '"+X+"'"
            try:
                cursor.execute(sql)
                print(cursor.fetchall()[0])
                public_key = cursor.fetchall()[0]
                print(public_key)
            except Exception as e:
                print("SQL exception", e)
            dbconnection.close()
            ACK_COUNTER += 1
            if ACK_COUNTER == 1:
                connection.sendall(bytes(nb1, "UTF-8"))
            else:
                connection.sendall(b"ACK")
                print("ACK sent")

            print("before receiving the second")
            clientMessageTwo = connection.recv(8192)
            print("after receiving the second")
            R1 = int(repr(clientMessageOne)[2:len(repr(clientMessageOne)) - 1])
            print("R1 is ", R1)

            if pow(GENERATOR, R1) == X*(pow(int(public_key), nb1)):
                print("True")
                connection.sendall(b'True')
            else:
                connection.sendall(b'False')
except Exception as ex:
    traceback.print_exc()
