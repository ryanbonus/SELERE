import os
import can
from datetime import datetime
import time
import threading

#Motor parameters
BITRATE = 500000
LOGGING_DELAY = 60 #In seconds, used to add a delay between logs so that redundant status updates don't clog the log and create a huge file. Todo, create a function that only allows unique logs to be written to file. Make that function append a time range to the previous log for clarity.

def write_log(log_text, log_dir="logs"):
    #print(log_text)  #for live debugging
    
    # Get the current date for the file name
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"{log_dir}/{date_str}.txt"

    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Get the current time to include with each entry
    time_str = datetime.now().strftime("%H:%M:%S")
    log_entry = f"{time_str} - {log_text}"

    # Append the log entry to the file, creating it if it doesn't exist
    with open(log_filename, "a") as log_file:
        log_file.write(log_entry + "\n")

def can_handler_thread(bus, jointMotors):
    #Continuously receive CAN messages and write them to log files
    while True:
        msg = bus.recv()  # Wait for a new message
        
        if msg:
            try:
                jointMotors[0].position = int((msg[44:46]+msg[47:49]), 16)
                jointMotors[0].speed = int((msg[50:52]+msg[53:55]), 16)
                jointMotors[0].current = int((msg[56:58]+msg[59:61]), 16)
                jointMotors[0].temp = int((msg[62:64]), 16)
                jointMotors[0].errorCode = int((msg[65:67]), 16)
            except Exception as e:
                print(f"Error extracting parameter, message: {e}")

            write_log(msg)
            time.sleep(LOGGING_DELAY) # This magic number changes the logging frequency. 


def comm_can_transmit_eid(bus, eid, data):
    # Ensure data length is within CAN limits
    if len(data) > 8:
        data = data[:8]
    
    # Create a CAN message
    message = can.Message(
        arbitration_id=eid,  # Extended ID
        is_extended_id=True, # Use extended ID
        data=data            # Data payload
    )
    
    # Send the message
    try:
        bus.send(message)
        print("Message sent on CAN bus")
    except can.CanError as e:
        print(f"Error sending message: {e}")

def demo_event_loop(canBus):
    while True:
        userInput=input("enter position")
        #Do something

def tkinter_loop(jointMotors, canBus, tkLoop):
    for component in jointMotors:
        component.canbus = canBus
    tkLoop()

def start_can(jointMotors, eventLoop, event):
    try:
        # Set up the CAN interface with the specified bitrate, This must match the Baud Rate parameter set in R-link
        write_log("Setting bitrate for can0...")
        os.system('sudo ip link set can0 type can bitrate '+str(BITRATE))
        write_log("Bringing can0 interface up...")
        os.system('sudo ip link set can0 up')  # Bring the interface up
        write_log("can0 interface is up.")

        # Create the CAN bus interface
        print("Initializing CAN bus...")
        can0 = can.interface.Bus(interface='socketcan', channel='can0')
        print("CAN bus initialized successfully.")

        # Create thread for receiving messages
        receiver_thread = threading.Thread(target=can_handler_thread, args=(can0, jointMotors), daemon=True)
        # Start the receiver thread
        receiver_thread.start()
        # CALL MAIN EVENT LOOP BELOW, MUST BE A FUNCTION WITH A CONSTANT LOOP & EXPECTING A PARAMETER 'canbus'
        eventLoop(jointMotors, can0, event)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Bring the interface down
        print("Bringing can0 interface down...")
        os.system('sudo ip link set can0 down')
        print("can0 interface is down.")