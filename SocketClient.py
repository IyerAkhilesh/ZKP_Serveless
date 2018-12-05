import socket
import threading
import traceback

import NumberGenerator_V0 as csprng
import pickle


file = open("shared.pkl", "rb")
uname_and_pass = pickle.load(file)
uname, pswd = uname_and_pass
username = uname[1]
password = pswd[1]
print(username, password)
HOST = "127.0.0.1"
SERVER_PORT_ONE = 3000
SERVER_PORT_TWO = 6000
SERVER_PORT_THREE = 9000
SERVER_PORT_FOUR = 12000

user_number = csprng.username_processor(username)
print(user_number)
user_number_factors = csprng.factorizer(user_number,1)
print(user_number_factors)
user_number_factors_one, user_number_factors_two = user_number_factors[0: user_number_factors.find(',')], user_number_factors[user_number_factors.find(',')+1:len(user_number_factors)]
# print(user_number_factors_one, user_number_factors_two)
pass_number = str(csprng.password_to_number(password))
print(pass_number)
X, Y, nb1, nb2 = 0, 0, 0, 0
resultOne=""
resultTwo=""

def sendToContainerOne():
    global X
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, SERVER_PORT_ONE))
            print("Sending n1 to Container server 1")
            sock.sendall(bytes(user_number_factors_one, "UTF-8"))  # Sends n1
            serverMessage = sock.recv(8192)
            if serverMessage.isalnum():
                X = repr(serverMessage)[2:len(repr(serverMessage)) - 1]
                print("Message sent by Container 1: ", repr(serverMessage)[2:len(repr(serverMessage)) - 1])
            else:
                print("Message sent by Container 1: ", repr(serverMessage)[2:len(repr(serverMessage)) - 1])
    except:
        traceback.print_exc()

def sendToContainerTwo():
    global Y
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_two:
            sock_two.connect((HOST, SERVER_PORT_TWO))
            print("Sending n2 to Container Server 2")
            sock_two.sendall(bytes(user_number_factors_two, "UTF-8"))       #Sends n2
            serverMessageTwo = sock_two.recv(8192)
            if serverMessageTwo.isalnum():
                Y = repr(serverMessageTwo)[2:len(repr(serverMessageTwo)) - 1]
                print("Message sent by Container 2: ", repr(serverMessageTwo)[2:len(repr(serverMessageTwo)) - 1])
            else:
                print("Message sent by Container 2: ", repr(serverMessageTwo)[2:len(repr(serverMessageTwo)) - 1])
    except:
        traceback.print_exc()

def sendToAuthenticatorOne():
    global nb1
    try:
        sock_three = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_three.connect((HOST, SERVER_PORT_THREE))
        print("Sending x to Authentication Server 1")
        sock_three.sendall(bytes(str(X), "UTF-8"))                           #Sends x
        serverMessageThree = sock_three.recv(8192)
        if serverMessageThree.isalnum():
            nb1 = int(repr(serverMessageThree)[2:len(repr(serverMessageThree)) - 1])
            print(nb1)
            print("Message 1 sent by Authenticator 1: ", repr(serverMessageThree)[2:len(repr(serverMessageThree)) - 1])
        else:
            print("Message 1 sent by Authenticator 1: ", repr(serverMessageThree)[2:len(repr(serverMessageThree)) - 1])

        R1 = str(nb1 * int(pass_number) + int(user_number_factors_one))           #Sends r1 = nb1*Sa + n1
        sock_three.sendall(bytes(R1, "UTF-8"))
        serverMessageThree = sock_three.recv(8192)
        print("Message 2 sent by Authenticator 1: ", repr(serverMessageThree)[2:len(repr(serverMessageThree)) - 1])

        serverMessageThree = sock_three.recv(8192)
        print("Message 3 sent by Authenticator 1: ", repr(serverMessageThree)[2:len(repr(serverMessageThree)) - 1])
        sock_three.close()

        resultOne = repr(serverMessageThree)[2:len(repr(serverMessageThree)) - 1]
        # return resultOne
    except Exception as ex:
        traceback.print_exc()

def sendToAuthenticatorTwo():
    global nb2
    try:
        sock_four = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_four.connect((HOST, SERVER_PORT_FOUR))
        print("Sending y to Authentication Server 2")
        sock_four.sendall(bytes(str(Y), "UTF-8"))                            #Sends y
        serverMessageFour = sock_four.recv(8192)
        if serverMessageFour.isalnum():
            nb2 = int(repr(serverMessageFour)[2:len(repr(serverMessageFour)) - 1])
            print(nb2)
            print("Message 1 sent by Authenticator 2: ", repr(serverMessageFour)[2:len(repr(serverMessageFour)) - 1])
        else:
            print("Message 1 sent by Authenticator 2: ", repr(serverMessageFour)[2:len(repr(serverMessageFour)) - 1])

        R2 = str(nb2*int(pass_number) + int(user_number_factors_two))
        sock_four.sendall(bytes(R2, "UTF-8"))                           #Sends r2 = nb2*Sa + n2
        serverMessageFour = sock_four.recv(8192)
        print("Message 2 sent by Authenticator 2: ", repr(serverMessageFour)[2:len(repr(serverMessageFour)) - 1])

        serverMessageFour = sock_four.recv(8192)
        print("Message 3 sent by Authenticator 2: ", repr(serverMessageFour)[2:len(repr(serverMessageFour)) - 1])
        sock_four.close()

        resultTwo = repr(serverMessageFour)[2:len(repr(serverMessageFour)) - 1]
        # return resultTwo
    except Exception as ex:
        traceback.print_exc()

def containerThreading():
    try:
        #Creating the threads
        thread_one = threading.Thread(sendToContainerOne())
        thread_two = threading.Thread(sendToContainerTwo())

        #Starting the threads
        thread_one.start()
        thread_two.start()

        #Waiting for the threads to fully complete execution
        thread_one.join()
        thread_two.join()

        #Print something when both threads are done executing
        print("Container threads 1 and 2 executed successfully")
    except:
        traceback.print_exc()

def authenticatorThreading():
    try:
        # #Creating the threads
        thread_three = threading.Thread((sendToAuthenticatorOne()))
        thread_four = threading.Thread(sendToAuthenticatorTwo())

        # #Starting the threads
        thread_three.start()
        thread_four.start()
        #
        # #Waiting for the threads to fully complete execution
        thread_three.join()
        thread_four.join()

        #Print something when both threads are done executing
        print("Authenticator threads 1 and 2 executed successfully")
    except:
        traceback.print_exc()

try:
    #Creating the threads
    thread_five = threading.Thread(containerThreading())
    thread_six = threading.Thread(authenticatorThreading())

    #Starting the threads
    thread_five.start()
    thread_six.start()

    # Waiting for the threads to fully complete execution
    thread_five.join()
    thread_six.join()

    # Print something when both threads are done executing
    print("Authenticator and Container threads executed successfully")

    if(resultOne == resultTwo):
        print("Login Successful!!")
    else:
        print("Login Unsuccessful!!")

except:
    traceback.print_exc()
