#==============================================================================
# Project: Robocar
# Application: Remote_Control
# File: main.py
# Version: 1.0
# Description: entry point for Remote_Control application: initializes queues 
# and processes (server and gui)
#==============================================================================

#==============================================================================
# Import
#==============================================================================

from multiprocessing import Process, Queue, Value
import time as time

import GUI as myGUI
import Server as myServer

#==============================================================================
# Global data
#==============================================================================




#==============================================================================
# Main flow
#==============================================================================

if __name__ == '__main__':
    
    # Shared data
    # Shared data: Misc
    server_state = Value("i", myServer.State.SOCK_CLOSED)
    # Shared data: Queues
    queue_2_car = Queue(1)    # To be improved: Pipe more convenient than Queue
    queue_from_car = Queue(1) # To be improved: Pipe more convenient than Queue
    queue_exit = Queue(1)   # This queue must never be consumed,
                            # only push data there and exit if full
    
    # Init processes
    proc_GUI = Process(target=myGUI.gui_main, 
        args=(queue_2_car, queue_from_car, queue_exit))
    proc_Server = Process(target=myServer.run_server, 
        args=(server_state, queue_from_car, queue_2_car, queue_exit))

    # Start processes
    proc_GUI.start()
    proc_Server.start()

    # Monitor processes
    while(1):
        # If message in exit queue, close main process
        if queue_exit.full() == True:
            print("Exiting from main...")
            break    # end app
        # Print server status
        # with server_state.get_lock():
        #     print("Server status: " + str(server_state.value))
        # Send debug (useless) information to car
        # if (queue_2_car.full() == False):    
        #     queue_2_car.put("0000010001200023000340004")
        # Print outgoing data 
        # if (queue_2_car.empty() == False):
        #     print(queue_2_car.get())
        # Print incoming data
        # if (queue_from_car.full() == False):
        #     print(queue_2_car.get())
        time.sleep(0.01)