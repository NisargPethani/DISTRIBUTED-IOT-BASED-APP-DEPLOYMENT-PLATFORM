import socket
import time
import random
ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2010
sensor_ip = '127.0.0.1'
sensor_port = 5501
print('Waiting for connection response')
flag_x = False

try:
    pass
    ClientMultiSocket.bind(('127.0.0.1', 5501))

except:
    pass



while True:
    try:
        # ClientMultiSocket.bind(('127.0.0.1', 5500))
        ClientMultiSocket.connect((host, port))
        # print('1')
        res = ClientMultiSocket.recv(1024)
        while True:
            try:
                # Input = input('Hey there: ')
                Input = 'Start'
                Input = 'Sensor2:' + str(random.randint(1, 50))
                Input = sensor_ip + ':::' + str(sensor_port) + ':::' + str(random.randint(1, 100))
                ClientMultiSocket.send(str.encode(Input))
                res = ClientMultiSocket.recv(1024)
                # print(res.decode('utf-8'))
                time.sleep(6)
            except:
                flag_x = True
                # print('3')
                # time.sleep(4)
                break

    except socket.error as e:
        if flag_x:
            ClientMultiSocket.close()
            ClientMultiSocket = socket.socket()
            ClientMultiSocket.bind(('127.0.0.1', 5501))
            # print('5')
            flag_x = False
        # print('4')
        # time.sleep(4)
        pass
        #print(str(e))











