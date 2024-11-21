import os
import can
import threading
import time
from datetime import datetime
import numpy as np
from enum import Enum

# CAN packet definitions
CAN_PACKET_SET_DUTY = 0
CAN_PACKET_SET_CURRENT = 1
CAN_PACKET_SET_CURRENT_BRAKE = 2
CAN_PACKET_SET_RPM = 3
CAN_PACKET_SET_POS = 4
CAN_PACKET_SET_ORIGIN_HERE = 5
CAN_PACKET_SET_POS_SPD = 6

def writeLog(log_text, log_dir="logs"):
    print(log_text)  #for live debugging
    
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

def canHandlerThread(bus):
    """Continuously receive CAN messages and write them to log files."""
    while True:
        msg = bus.recv()  # Wait for a new message
        if msg:
            writeLog(msg)
            time.sleep(1)


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

def buffer_append(nBytes, bufferObject, number, startingPos):
    firstshift = (nBytes-1)*8
    number = np.int32(number)
    for i in range(0,nBytes):
        temp = (number >> firstshift-i*8) & 0xFF
        bufferObject.append(temp)

def buffer_append_int32(buffer, number, index): #To-do, Delete this function and replace with calls to buffer_append
    buffer_append(4,buffer,number,index)

def buffer_append_int16(buffer, number, index): #To-do, Delete this function and replace with calls to buffer_append
    buffer_append(2,buffer,number,index)

def position_speed_accelleration(controller_id, bus, position, speed, rpa):
    position_index = 0
    speed_index = 4
    rpa_index = 6
    buffer = bytearray(0)
    buffer_append_int32(buffer, np.int32(position*10000), position_index)
    buffer_append_int16(buffer, speed/10, speed_index)
    buffer_append_int16(buffer, rpa/10, rpa_index)
    eid = (controller_id | int(CAN_PACKET_SET_POS_SPD) << 8)
    comm_can_transmit_eid(bus, eid, buffer)    

def eventLoop(canBus):
    while True:
        userInput=input("enter position")
        if userInput:
            position_speed_accelleration(1, canBus, int(userInput), 6000, 3000)


def startCan(eventLoop):
    try:
        # Set up the CAN interface with the specified bitrate
        writeLog("Setting bitrate for can0...")
        os.system('sudo ip link set can0 type can bitrate 500000')
        writeLog("Bringing can0 interface up...")
        os.system('sudo ip link set can0 up')  # Bring the interface up
        writeLog("can0 interface is up.")

        # Create the CAN bus interface
        print("Initializing CAN bus...")
        can0 = can.interface.Bus(interface='socketcan', channel='can0')
        print("CAN bus initialized successfully.")

        # Create thread for receiving messages
        receiver_thread = threading.Thread(target=canHandlerThread, args=(can0,), daemon=True)
        # Start the receiver thread
        receiver_thread.start()
        # CALL MAIN EVENT LOOP BELOW, MUST BE A FUNCTION WITH A CONSTANT LOOP
        eventLoop(can0)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Bring the interface down
        print("Bringing can0 interface down...")
        os.system('sudo ip link set can0 down')
        print("can0 interface is down.")

#def extend(rangeOfMotionTop, rangeOfMotionBottom):

startCan(eventLoop)