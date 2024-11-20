import os
import can
import threading
import time
from datetime import datetime

# Constants for limits
P_MIN = -12.5
P_MAX = 12.5
V_MIN = -50.0
V_MAX = 50.0
T_MIN = -65.0
T_MAX = 65.0
Kp_MIN = 0
Kp_MAX = 500.0
Kd_MIN = 0
Kd_MAX = 5.0

def float_to_uint(x, x_min, x_max, bits):
    """Converts a float to an unsigned int given the range and number of bits."""
    span = x_max - x_min
    x = max(min(x, x_max), x_min)
    return int((x - x_min) * ((1 << bits) / span))

def pack_cmd(p_des, v_des, kp, kd, t_ff):
    """Pack command into a CAN message."""
    p_int = float_to_uint(p_des, P_MIN, P_MAX, 16)
    v_int = float_to_uint(v_des, V_MIN, V_MAX, 12)
    kp_int = float_to_uint(kp, Kp_MIN, Kp_MAX, 12)
    kd_int = float_to_uint(kd, Kd_MIN, Kd_MAX, 12)
    t_int = float_to_uint(t_ff, T_MIN, T_MAX, 12)

    # Pack ints into the CAN message data
    msg_data = bytearray(8)
    msg_data[0] = p_int >> 8  # Position High 8
    msg_data[1] = p_int & 0xFF  # Position Low 8
    msg_data[2] = v_int >> 4  # Speed High 8 bits
    msg_data[3] = ((v_int & 0xF) << 4) | (kp_int >> 8)  # Speed Low 4 bits, KP High 4 bits
    msg_data[4] = kp_int & 0xFF  # KP Low 8 bits
    msg_data[5] = kd_int >> 4  # Kd High 8 bits
    msg_data[6] = ((kd_int & 0xF) << 4) | (t_int >> 8)  # Kd Low 4 bits, Torque High 4 bits
    msg_data[7] = t_int & 0xFF  # Torque Low 8 bits

    return msg_data

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

def send_can_message(bus, command):
    """Takes in a byteArray of size 8, and sends it to the motor as a can message"""
    formattedCommand = can.message(arbitration_ID=0x01, data=command, is_extended_id=False)
    bus.send(command)

def startCan():
    try:
        # Set up the CAN interface with the specified bitrate
        writeLog("Setting bitrate for can0...")
        os.system('sudo ip link set can0 type can bitrate 1000000')
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
        

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Bring the interface down
        print("Bringing can0 interface down...")
        os.system('sudo ip link set can0 down')
        print("can0 interface is down.")

#def extend(rangeOfMotionTop, rangeOfMotionBottom):

startCan()