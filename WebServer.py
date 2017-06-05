#import socket module
from socket import *
import ssl
from ssl import *
serverSocket = socket(AF_INET, SOCK_STREAM)

ssl.wrap_socket(serverSocket, keyfile="server.key", certfile="server.crt", server_side=True, cert_reqs=CERT_NONE,ca_certs=None, do_handshake_on_connect=True, suppress_ragged_eofs=True, ciphers="AES128-SHA256")
"""
Prepare a sever socket 
"""
serverPort = 443

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))

# Listen to at most 1 connection at a time
serverSocket.listen(1)

while True: 
    #Establish the connection 
	print ('Ready to serve...') 
	connectionSocket, addr = serverSocket.accept()
	try:
		message =  (connectionSocket.recv(1024)).decode('utf-8')
		filename = message.split()[1]

		f = open(filename[1:],'rb')
		outputdata = f.read()
		f.close()
		
		"""
		Send HTTP header line(s) into socket 
		Note: With send(), strings must be encoded into utf-8 first using encode('utf-8') 
		"""
		connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n')

        #Send the content of the requested file to the client 
		connectionSocket.send(outputdata)

		connectionSocket.send(b'\r\n')

 
		# Close the client connection socket
		connectionSocket.shutdown(SHUT_RDWR)
		connectionSocket.close() 

	except IOError: 
		"""
		Send response message for file not found
		"""
		connectionSocket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
		connectionSocket.send(b'<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n')

		"""
		Close client socket 
		"""
		connectionSocket.shutdown(SHUT_RDWR)
		connectionSocket.close() 

serverSocket.close() 
