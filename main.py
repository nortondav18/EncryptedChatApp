import socket
import threading

import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner_key = None



#
choice = input("Do you want to be a server or a client? (s/c): ")

if  choice == "s":
    # Server
    print("Starting server...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #get ip - ipconfig ethernet ipv4
    #your ip here
    serverIP = socket.gethostbyname(socket.gethostname())
    print("Your IP is: " + serverIP)
    
    server.bind((serverIP, 9999))
    server.listen(1)
    
    print("Waiting for a connection...")
    client, address = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner_key = rsa.PublicKey.load_pkcs1(client.recv(1024), "PEM")
    print("Connected to " + str(address))
    
elif choice == "c":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #the person you want to talk to ip
    # in this case client and server are on the same computer
    choice2 = input("what is the ip of the server you wish to connect to? 1 for localhost:")
    if choice2 == "1":
        serverIP = socket.gethostbyname(socket.gethostname())
    else:
        serverIP = choice2
    print("Connecting to " + serverIP)
    client.connect((serverIP, 9999))
    public_partner_key = rsa.PublicKey.load_pkcs1(client.recv(1024), "PEM")
    client.send(public_key.save_pkcs1("PEM"))
    print("Connected to " + serverIP)
    
else:
    print("Invalid choice")
    exit()
    
    
def sending_Messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode("utf-8"), public_partner_key))
        print("You: " + message)
        
def receiving_Messages(c):
    while True:
        print("Partner: " + rsa.decrypt(c.recv(1024), private_key).decode("utf-8"))
        
sendThread = threading.Thread(target=sending_Messages, args=(client,))
receiveThread = threading.Thread(target=receiving_Messages, args=(client,))

sendThread.start()
receiveThread.start()
