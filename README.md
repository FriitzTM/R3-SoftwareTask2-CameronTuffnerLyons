# R3-SoftwareTask2-CameronTuffnerLyons

This Project was created as part of Software training task 2 F2021 for Ryerson Rams Robotics.

Firstly I would like to say that this past two weeks have been nothing but bad days which included three midterms and my computer breaking so I ended up doing this project in one day (the day it was due) so I apologise if this is not as clean as it could be or if it looks very rushed(it was sadly).

The main objective of this project was be able to control 4 motors on a rover by using a client and server that would communicate both the pwm values as well as the direction of spin of the 4 motors on the rover. this was to be done in python.

THE CLIENT:

![image](https://user-images.githubusercontent.com/83479899/138613224-30c21fcf-7a11-4f7d-895a-645398c97f09.png)

This project uses pynput keyboard to monitor key strokes and allow you to communicate to the server.
This project also uses the socket and selector libraries to control tcp communication.
types is just used to process the data being sent/recieved.

The sockets are using the localhost ip (127.0.0.1) and port 65432.

![image](https://user-images.githubusercontent.com/83479899/138613269-6354d3f7-41a7-4074-a865-abb8ac10d071.png)

since I was short on time I decided to just uses global variables to keep track of the all the info i needed, which was just speed/pwm value and direction. The output variable is used later for sending the information to the server.

![image](https://user-images.githubusercontent.com/83479899/138614906-7f86afe7-2091-4191-8659-5bd6034a53c0.png)

The start_connections function initializes the socket needed for tcp communication and places the default outbound message into the data object, which also carries information on the length of the message as well as some variables that will be used in other functions.

![image](https://user-images.githubusercontent.com/83479899/138615007-f6506f91-4b80-4a0e-b7fa-c5c4f0893532.png)

the service_connection function updates the outbound message and then uses the outb variable of the data object as passthrough for the message which is then sent to the server

start_connections runs first.

on_press, on_release, and the keyboard listener are used to detect and process key strokes and determine either the direction or the speed needs to be chenged.

![image](https://user-images.githubusercontent.com/83479899/138615172-01c2c88c-17cb-4afb-9e59-f30c2e7488b6.png)

If the user is trying to change the speed they must press numbers 0-5, this will update the global speed variable and print feedback on the client. 
The function sendData is then called.

![image](https://user-images.githubusercontent.com/83479899/138615227-9dbb3267-423e-419e-ae8f-794fd1de1d56.png)

If the user wishes to change the direction then they must press one of the arrow keys. Depending on which arrow key is pressed, the char array called direction will be modified to represent the desired direction. The sendData function is then called.

![image](https://user-images.githubusercontent.com/83479899/138615379-6be08e7f-094f-4e86-96ab-8dfcfb6a7c2d.png)

The send data function constructs the outbound string which is then converted to bytes before running the service_connection function to send the data to the server.

![image](https://user-images.githubusercontent.com/83479899/138615458-782778bd-deeb-4aa0-99e1-662eba1b328a.png)

The on_release function is a placeholder that serves no purpose for this project other than to ensure that the keyboard listener functions properly.

THE SERVER:

The server uses the same imports as the client minus pynput.
the host ip and port are also the same.

![image](https://user-images.githubusercontent.com/83479899/138615529-a038d447-39e7-4698-ae16-a35f661aa349.png)

The server initializes a socket and begins listening for the client to connect.

![image](https://user-images.githubusercontent.com/83479899/138615552-aa06b13d-5ae3-46b1-bf20-906c2cf32090.png)

the accept_wrapper function accepts the incomming connection from the client and creates the required objects and variables to be used in other parts of the code.

![image](https://user-images.githubusercontent.com/83479899/138615591-bb18f2fc-9d04-4f28-864b-fc3dac8edfd2.png)

The service_connection function recieves the incoming data and decodes bytes into a string which can be printed on the server. It also check to see if the client has disconnected, and if they have, it will stop the server.

![image](https://user-images.githubusercontent.com/83479899/138615755-d5b03b5d-5af3-4de5-ac99-1d59e7115424.png)

The loopback interface detects incomming data or a new connection and calls upon the relevent function, either accept_wrapper or service_connection

SAMPLE INPUT:

![image](https://user-images.githubusercontent.com/83479899/138616180-2c6aa5e6-b1b8-44d4-b7b5-cd9e3c7df141.png)


CORRESPONDING OUTPUT:

![image](https://user-images.githubusercontent.com/83479899/138616195-6a7caa39-4c0e-4ad2-a381-7d5562739d66.png)

