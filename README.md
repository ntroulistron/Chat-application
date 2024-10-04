# Chat-application


Chat Application

I am asked to build an application in socket python programming regarding a client and a server. My code is written in VSCODE, and I have used different functionalities and definitions in my code in order to make it as it is right now. The purpose of my code is to make clients connect to server sockets and make them able to chat with one another. I’m a University of Derby student, and this is my Chat Application documentation. 

			SERVER CODE
Basic Logging Setup:
To start with, my server code begins with a basic logging setup. This section establishes the foundation for monitoring and recording server activities. It configures the logging level, ensuring that all relevant information, including debugging details, is captured for analysis and troubleshooting. 

Server Configuration:
Here, the server's essential parameters such as the host address, port number, and maximum number of allowed incoming connections are defined. This setup is crucial for establishing the basic network identity and operational limits of the server.
 
	
	Client Tracking Dictionary:
	This part of the code creates a structure to manage and track the connected clients. It's a critical component for maintaining active client sessions, enabling the server to efficiently manage multiple client connections simultaneously.
 

	Encryption Key Generation:
	In this segment, a Fernet key is generated for encrypting communications, emphasizing the server's commitment to security. This encryption key is central to ensuring that data transferred between the server and clients remains confidential and tamper-proof.
 

	Server Action Logging Function:
	This function is dedicated to maintaining a detailed log of server actions. It not only records these actions to a file for persistent tracking but also prints them to the console for real-time monitoring, enhancing the server's transparency and accountability.
 

	Client Authentication Function:
	This function is pivotal in verifying the identity of clients. By checking usernames and passwords against a list of valid credentials, it ensures that only authorized users can access the server, thereby safeguarding the system against unauthorized access.
 

	Broadcast Message Function:
	Central to the server's communication capabilities, this function enables the broadcasting of messages to all connected clients or a targeted recipient. This feature is essential for disseminating information efficiently across the network.
 
	
	Individual Client Handler Function:
	This segment deals with the nuances of individual client-server interactions. It sets up secure communication channels using SSL and manages message reception and broadcasting, playing a key role in maintaining smooth and secure client interactions.
 
 
	Direct Message Sending Function:
	This function facilitates private communication between clients. By allowing messages to be sent to specific clients, it adds a layer of personalization and privacy to the server's communication capabilities.
 

	Server Start Function:
	The main function is to initiate the server's operations. It binds the server to the specified host and port, listens for incoming connections, and manages client sessions, thereby acting as the operational core of the server.
 


				CLIENT CODE
	Basic Logging Configuration:
	This section sets up basic logging for the client, ensuring that all operations and events are recorded for future analysis. This is crucial for debugging and understanding the client's behavior in different scenarios.
 
	
	P2PClient Class Initialization:
	The core of my client application, this class initializes the necessary components for a peer-to-peer client, including SSL context for secure connections, client socket, login status, symmetric key for encryption, and a list of peer addresses.
 

	Client Action Logging Function:
	This method encrypts and logs client actions into a file, maintaining a secure and tamper-proof record of all actions performed by the client. This is key for auditing and security purposes.
 

	Peer List Management:
	This functionality updates the client's knowledge of peers in the network. It's crucial for maintaining an up-to-date list of available peers for communication, ensuring the client can efficiently connect to others in the network.
 

	Peer Connection Method:
	This method establishes a direct connection to another peer. It's essential for peer-to-peer communication, allowing the client to interact and exchange information with other nodes in the network.
 

	Server Connection Method:
	This part of the code is responsible for connecting the client to a central server. It's a critical component for initial communications and key exchanges, setting the stage for secure, encrypted interactions.
 

	Client Logging Process:
	The login method handles user authentication with the server. It involves sending encrypted credentials and interpreting the server's response, determining the success or failure of the login attempt. This process is fundamental for access control and user verification.
 

	Message Sending Function:
	This function allows the client to send encrypted messages to the server. It's a key part of the client's functionality, enabling the user to communicate securely with the server or other clients.
 

	Direct Message Functionality:
	This feature provides the capability to send direct messages to specific recipients, adding a layer of personalized communication to the client's capabilities.
 

	Message Reception and Decryption:
	The client continuously listens for incoming messages from the server, decrypting and displaying them to the user. This is a vital aspect of the client's functionality, ensuring that incoming communication is promptly and securely received.
 

	Main Execution Block:
	This is the starting point of the client application. It initiates the connection to the server, handles the login process, and enters the main chat loop where the client can send and receive messages. This block orchestrates the overall workflow and user interaction of the client program.
 

     Screenshot after running the program:

Server output:
 
Client output after successful connection:
 
Server output after successful authentication and message sent:
 
Client output after authentication failed:
 
Server output after authentication failed:
 
Client output after user disconnects:
 

					
		            Other tools used in the application.
	
Generate_certificate.py:
 

Server-cert.pem:
 

Server-key.pem:
 

Action_log.txt:
 

		                

	
	
