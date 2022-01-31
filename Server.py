#==============================================================================
# Project: Robocar
# Application: Remote_Control
# File: Server.py
# Description: This file takes charge of initialising a server, listen to the 
# incoming messages and send them back via queues
#==============================================================================

#==============================================================================
# Import
#==============================================================================

import socket
from multiprocessing import Value, Queue
import time

#==============================================================================
# Global data
#==============================================================================

DEBUG_EN = True

# Server parameters
HOST_IP = '192.168.0.1'
HOST_PORT = 60000
TIMEOUT_SEC = 6

#==============================================================================
# Classes
#==============================================================================

class State():
    SOCK_CLOSED = 0
    SOCK_LISTENING = 1
    CONN_OPEN = 2
    CONN_ERROR = 3


#==============================================================================
# Function definitions
#==============================================================================

def _init_socket(server_state_out:Value) -> socket.socket:
    """
    Initialises a TCP socket with globally-defined HOST_IP and HOST_PORT

    :param server_state_out: Status report. Check class State for more info
    :type server_state_out: (Value(int)) from multiprocessing
    :return: my_socket
    :rtype: (socket.socket)
    """

    # Create a TCP/IP socket (AF_INET for IPv4, SOCK_STREAM for TCP)
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Bind the socket to the port
    server_address = (HOST_IP, HOST_PORT)
    if DEBUG_EN:
        print('Server: starting up on {} port {}'.format(*server_address))
    my_socket.bind(server_address)
    # Listen for incoming connections
    my_socket.listen()
    with server_state_out.get_lock():
        server_state_out.value = State.SOCK_LISTENING
    # Return
    return my_socket

def _new_connection(my_socket:socket.socket, server_state_out:Value) \
        -> (socket.socket):
    """
    Waits for a connection to a client to be established and sets a TIMEOUT_SEC
    on this connection

    :param my_socket: socket previosly initialised
    :type my_socket: (socket.socket)
    :param server_state_out: Status report. Check class State for more info
    :type server_state_out: (Value(int)) from multiprocessing
    :return: connection already established
    :rtype: (socket.socket)
    """

    if DEBUG_EN: print('Server: waiting for a connection')
    connection, client_address = my_socket.accept()
    if DEBUG_EN: print('Server: connection from', client_address)
    connection.settimeout(TIMEOUT_SEC)
    with server_state_out.get_lock():
        server_state_out.value = State.CONN_OPEN
    return connection

def _close_connection(connection:socket.socket, server_state_out:Value):
    """
    Closes the connection

    :param connection: connection to be closed
    :type connection: (socket.socket)
    :param server_state_out: Status report. Check class State for more info
    :type server_state_out: (Value(int)) from multiprocessing
    """

    connection.close()
    with server_state_out.get_lock():
        server_state_out.value = State.CONN_ERROR

def run_server( server_state_out:Value, queue_from_car:Queue(1), 
                queue_2_car:Queue(1), queue_exit:Queue(1)):
    """
    Initialises TCP socket with global parameters, create and attend a 
    connection from client. Reconnection is done if any error occurs.
    
    :param server_state_out: allows reporting the status of the server to other
    processes. Check class State for more information
    :type server_state_out: (Value(int)) from multiprocessing
    :param queue_from_car: when an element is received from the car, it is 
    stored here as str
    :type queue_from_car: Queue(1) from multiprocessing
    :param queue_2_car: when a str message comes via this queue, it is taken and 
    sent to the car
    :type queue_2_car: Queue(1) from multiprocessing
    :param queue_exit: the function finishes if the queue stores ANY element
    :type queue_exit: Queue(1) from multiprocessing
    :exceptions: any exception raised during this function leads to a reset
    in the connection
    """

    my_socket = _init_socket(server_state_out)
    while True:
        # If message in exit queue, close process
        if queue_exit.full() == True:
            break
        # Create new connection
        connection = _new_connection(my_socket, server_state_out)
        # Attend the connection
        try:    
            while True:
                # If message in exit queue, close process
                if queue_exit.full() == True:
                    if DEBUG_EN: print("Exiting from Server...")
                    break
                # Receive the data in chunks of 1024 bytes
                data = connection.recv(1024)
                if data:
                    queue_elem = str(data.decode())
                    if (queue_from_car.full() == True):
                        queue_from_car.empty()  # Only most recent data is valid
                    queue_from_car.put(queue_elem)
                    if DEBUG_EN:
                        received_str = ""
                        for i in range(0,len(queue_elem),5):
                            received_str += queue_elem[i:i+5] + ','
                        print('Server / received: ' + received_str)
                # Send data from queue
                while(queue_2_car.empty() == False):
                    data_2_send = bytes(queue_2_car.get(), 'utf-8')
                    connection.sendall(data_2_send)
                    if DEBUG_EN:
                        sent_str = ""
                        for i in range(0,len(data_2_send.decode()),5):
                            sent_str += data_2_send.decode()[i:i+5] + ','
                        print("Server / sent: " + sent_str) 
        # Timeout. Wait for new conection
        except:
            _close_connection(connection, server_state_out) 

            


