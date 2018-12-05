import math
import socket
import traceback

from numpy import long

import NumberGenerator_V0 as csprng
import pymysql

HOST = "127.0.0.1"
PORT = 12000
ACK_COUNTER = 0
GENERATOR = 2
power_counter = 9
Nb = math.floor(pow(6, math.e * power_counter / 2)) % 100000000
Nb_factors = csprng.factorizer(Nb,0)
nb2 = Nb_factors[Nb_factors.find(',')+1:len(Nb_factors)]
print("Nb2", nb2)

dbconnection = pymysql.connect(host="localhost", port=3306, user="root", passwd="Akhilesh@1997", db="user_information")
cursor = dbconnection.cursor()

def power(base, exponent):
    raised = long(1)
    print(base, exponent)
    try:
        for _ in range(long(exponent)):
            raised *= long(base)
    except Exception as e:
        print(e)
        traceback.print_exc()
    print(raised)
    return str(raised)

global pkey, Y

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:     #automatically closes sock at the end of the block
        sock.bind((HOST, PORT))
        sock.listen(5)
        print("before accept")
        connection, address = sock.accept()
        print("after accept")

        with connection:                                                #automatically closes connection at the end of the block
            print("Connected to: ", address)
            while True:
                clientMessage = connection.recv(1024)
                if clientMessage:
                    ACK_COUNTER += 1
                    if ACK_COUNTER == 1:
                        Y = repr(clientMessage)[2:len(repr(clientMessage)) - 1]
                        print(Y, nb2)
                        sql = "SELECT public_key FROM credentials where Y = '"+Y+"'"
                        try:
                            cursor.execute(sql)
                            pkey = str(cursor.fetchall()[0])
                            pkey = pkey[2:len(pkey) - 3]
                        except Exception as e:
                            print("Public Key: ", pkey)
                            print("SQL exception", e)
                        dbconnection.close()
                        connection.sendall(bytes(nb2, "UTF-8"))
                    else:
                        connection.sendall(b"ACK0\n")
                        R2 = repr(clientMessage)[2:len(repr(clientMessage)) - 1]
                        print("Public Key: ", pkey)
                        print("R2", R2)
                        print("First argument: ", power(GENERATOR, R2))
                        print("\nSecond argument: ", str(long(Y) * long(power(str(pkey[1:len(pkey) - 1]), nb2))))
                        if power(GENERATOR, R2) == str(long(Y) * long(power(str(pkey), nb2))):
                            connection.sendall(b"True")
                        else:
                            connection.sendall(b"False")
                else:
                    break
except Exception as exceptions:
    traceback.print_exc()