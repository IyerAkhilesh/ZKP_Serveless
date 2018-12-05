import traceback
import pymysql
import math
import socket
import NumberGenerator_V0 as csprng


HOST = "127.0.0.1"
PORT = 12000
ACK_COUNTER = 0
GENERATOR = 7
power_counter = 12
Nb = math.floor(pow(41, math.e * power_counter / 2)) % 100000000
Nb_factors = csprng.factorizer(Nb)
nb2 = Nb_factors[Nb_factors.find(',')+1:len(Nb_factors)]

# print("before dbconnection")
dbconnection = pymysql.connect(host="localhost", port=3306, user="root", passwd="Akhilesh@1997", db="user_information")
cursor = dbconnection.cursor()
# print("after dbconnection")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:     #automatically closes sock at the end of the block
        # print("before bind")
        sock.bind((HOST, PORT))
        # print("after bind")
        sock.listen(3)
        # print("after listen")
        connection, address = sock.accept()
        print("after accept", connection)
        with connection:                                                #automatically closes connection at the end of the block
            print("Connected to: ", address)
            global public_key
            # while True:
            clientMessageOne = connection.recv(8192)
            # if clientMessage:
            Y = repr(clientMessageOne)[2:len(repr(clientMessageOne)) - 1]
            print("Y", Y)
            # print("First", repr(clientMessage)[2:len(repr(clientMessage)) - 1])
            sql = "SELECT public_key FROM credentials"
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
                connection.sendall(bytes(nb2, "UTF-8"))
            else:
                connection.sendall(b"ACK")
                print("ACK sent")

            print("before receiving the second")
            clientMessageTwo = connection.recv(8192)
            print("after receiving the second")
            R2 = int(repr(clientMessageOne)[2:len(repr(clientMessageOne)) - 1])
            print("R2 is ", R2)

            if pow(GENERATOR, R2) == Y*(pow(int(public_key), nb2)):
                print("True")
                connection.sendall(b'True')
            else:
                connection.sendall(b'False')
except Exception as ex:
    traceback.print_exc()