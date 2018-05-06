# Message Receiver
from socket import *
import ics
host = "192.168.2.24" # this computer
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

def resetData():
    global data
    data=""

def generateICSFile(data):
    firstName=data[0]
    lastName=data[1]
    phoneNumber=data[2]
    dataFile=open("followup.dat","a")
    dataFile.write(firstName+"*"+lastName+"*"+phoneNumber+"\n")
    dataFile.close()








print ("Waiting to receive messages...")
while True:
    (data, addr) = UDPSock.recvfrom(buf)

    data = data.decode("utf-8")

    if data != "":
        generateICSFile(data)
        resetData()
        time.sleep(3)

UDPSock.close()
