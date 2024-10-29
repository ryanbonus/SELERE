import os
import can
import threading
import time



# Constants for limits
P_MIN = -95.5
P_MAX = 95.5
V_MIN = -30.0
V_MAX = 30.0
T_MIN = -18.0
T_MAX = 18.0
Kp_MIN = 0
Kp_MAX = 500.0
Kd_MIN = 0
Kd_MAX = 5.0
I_MAX = 30.0  # Example value for current limits

mid=0x01
exid = False

# Define control modes
CONTROL_MODE = {
    "DUTY_CYCLE": 0,
    "CURRENT_LOOP": 1,
    "CURRENT_BRAKE": 2,
    "VELOCITY_MODE": 3,
    "POSITION_MODE": 4,
    "SET_ORIGIN_MODE": 5,
    "POS_VELOCITY_LOOP": 6
}

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

def pack_get_params_cmd():
    """Pack command to get motor parameters."""
    msg_data = bytearray([0x02, 0x01, 0x04, 0x40, 0x84, 0x03])  # Example command
    return msg_data

def unpack_reply(msg):
    """Unpack CAN message data."""
    id = msg.data[0]  # Driver ID
    p_int = (msg.data[1] << 8) | msg.data[2]  # Motor Position Data
    v_int = (msg.data[3] << 4) | (msg.data[4] >> 4)  # Motor Speed Data
    t_int = ((msg.data[4] & 0xF) << 8) | msg.data[5]  # Torque Data
    temperature = msg.data[6] - 40  # Assuming temperature range adjustment

    # Convert ints to floats
    position = uint_to_float(p_int, P_MIN, P_MAX, 16)
    speed = uint_to_float(v_int, V_MIN, V_MAX, 12)
    torque = uint_to_float(t_int, T_MIN, T_MAX, 12)

    return id, position, speed, torque, temperature

def uint_to_float(x_int, x_min, x_max, bits):
    """Convert unsigned int to float given range and number of bits."""
    span = x_max - x_min
    return (float(x_int) * span / float((1 << bits) - 1)) + x_min

def receive_can_messages(bus):
    """Continuously receive CAN messages."""
    while True:
        msg = bus.recv()  # Wait for a new message
        if msg:
            if msg.arbitration_id == mid or msg.arbitration_id == 1 :
                print(f"Full CAN message received: ID: {msg.arbitration_id}, Data: {[hex(byte) for byte in msg.data]}")
                id, position, speed, torque, temperature = unpack_reply(msg)
                print(f"Parsed CAN message - ID: {id}, Position: {position:.2f}, Speed: {speed:.2f}, Torque: {torque:.2f}, Temperature: {temperature:.2f}")
                time.sleep(1)  # Slow down message reception if necessary
            else: 
                # continue
                print(f"ID: {msg.arbitration_id}, {hex(msg.arbitration_id)} {bin(msg.arbitration_id)}")
                print(f"Full CAN message received: ID: {msg.arbitration_id}, Data: {[hex(byte) for byte in msg.data]}")

def enter_motor_control_mode(bus):
    """Send command to enter motor control mode."""
    msg_data = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC])
    msg = can.Message(arbitration_id=mid, data=msg_data, is_extended_id=exid)
    print(msg)
    bus.send(msg)
    print("Entered Motor Control Mode.")

def exit_motor_control_mode(bus):
    """Send command to exit motor control mode."""
    msg_data = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFD])
    msg = can.Message(arbitration_id=mid, data=msg_data, is_extended_id=exid)
    print(msg)
    bus.send(msg)
    print("Exited Motor Control Mode.")

def set_zero_position(bus):
    """Send command to set the current motor position as zero position."""
    msg_data = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE])
    msg = can.Message(arbitration_id=mid, data=msg_data, is_extended_id=exid)
    print(msg)
    bus.send(msg)
    print("Set current motor position as zero.")

def send_command(bus):
    """Wait for user input and send commands based on input."""
    while True:
        user_input = input("Enter '1' to set parameters, '2' to get motor parameters, '3' to move to position, '0' to enter control mode, '9' to exit control mode, '6' to set zero position, or 'q' to quit: ")
        if user_input == '1':
            p_des = float(input("Enter desired position: "))
            v_des = float(input("Enter desired velocity: "))
            kp = float(input("Enter proportional gain (Kp): "))
            kd = float(input("Enter derivative gain (Kd): "))
            t_ff = float(input("Enter feedforward torque: "))

            msg_data = pack_cmd(p_des, v_des, kp, kd, t_ff)
            msg = can.Message(arbitration_id=mid, data=msg_data, is_extended_id=exid)
            bus.send(msg)
            print("CAN message sent:")
            print(f"  Arbitration ID: 0x{msg.arbitration_id:X}")
            print(f"  Data: {[hex(byte) for byte in msg.data]}")
        elif user_input == '2':
            msg_data = pack_get_params_cmd()
            msg = can.Message(arbitration_id=mid, data=msg_data, is_extended_id=exid)
            bus.send(msg)
            print("Request to get motor parameters sent:")
            print(f"  Arbitration ID: 0x{msg.arbitration_id:X}")
            print(f"  Data: {[hex(byte) for byte in msg.data]}")
        elif user_input == '3':
            position = float(input("Enter desired position (degrees): "))
            move_to_position(bus, position)
        elif user_input == '0':
            enter_motor_control_mode(bus)
        elif user_input == '9':
            exit_motor_control_mode(bus)
        elif user_input == '6':
            set_zero_position(bus)
        elif user_input == '5':
            msg_data = [0xFF]*7+[0xFC]
            msg = can.Message(arbitration_id=mid, data=msg_data, is_extended_id=exid)
            bus.send(msg)
            print("CAN message sent:")
            print(f"  Arbitration ID: 0x{msg.arbitration_id:X}")
            print(f"  Data: {[hex(byte) for byte in msg.data]}")
            time.sleep(1)
            msg_data = [0x05,0x5c,0xd0,0x00,0x00,0x00,0x13,0x88]
            msg = can.Message(arbitration_id=mid, data=msg_data, is_extended_id=exid)
            bus.send(msg)
            print("CAN message sent:")
            print(f"  Arbitration ID: 0x{msg.arbitration_id:X}")
            print(f"  Data: {[hex(byte) for byte in msg.data]}")
            time.sleep(1)
            msg_data = [0x10,0x2b,0xb8,0x00,0x00,0x00,0x13,0x88]
            msg = can.Message(arbitration_id=mid, data=msg_data, is_extended_id=exid)
            bus.send(msg)
            print("CAN message sent:")
            print(f"  Arbitration ID: 0x{msg.arbitration_id:X}")
            print(f"  Data: {[hex(byte) for byte in msg.data]}")
            time.sleep(1)
        elif user_input == '7':
                msg_data = [0x00,0x00,0x00,0x00, 0x00, 0x0A, 0x00, 0x00]
                msg = can.Message(arbitration_id=0x0401, data=msg_data, is_extended_id=True)
                bus.send(msg)
                print("CAN message sent:")
                print(f"  Arbitration ID: 0x{msg.arbitration_id:X}")
                print(f"  Data: {[hex(byte) for byte in msg.data]}")
        elif user_input == '8':
            
            msg_data = [0x05,0x5c,0xd0,0x00,0x00,0x00,0x13,0x88]
            msg = can.Message(arbitration_id=0x0401, data=msg_data, is_extended_id=True)
            bus.send(msg)
            print("CAN message sent:")
            print(f"  Arbitration ID: 0x{msg.arbitration_id:X}")
            print(f"  Data: {[hex(byte) for byte in msg.data]}")
            time.sleep(1)
            msg_data = [0x10,0x2b,0xb8,0x00,0x00,0x00,0x13,0x88]
            msg = can.Message(arbitration_id=0x0401, data=msg_data, is_extended_id=True)
            bus.send(msg)
            print("CAN message sent:")
            print(f"  Arbitration ID: 0x{msg.arbitration_id:X}")
            print(f"  Data: {[hex(byte) for byte in msg.data]}")
            time.sleep(1)
        elif user_input.lower() == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid input. Please enter '1', '2', '3', '0', '9', '6', or 'q'.")

def move_to_position(bus, position_degrees):
    """Move motor to a specified position."""
    position_internal = position_degrees * 1000000.0  # Scale according to your protocol
    controller_id = mid  # Replace with your actual controller ID

    # Pack the command
    send_index = 0
    buffer = bytearray(8)
    buffer_append_int32(buffer, int(position_internal), send_index)

    # Send the position command
    comm_can_transmit_eid(controller_id | (CONTROL_MODE["POSITION_MODE"] << 8), buffer, send_index)

    print(f"Command sent to move to {position_degrees} degrees.")

def buffer_append_int32(buffer, number, index):
    """Append a 32-bit integer to the buffer."""
    buffer[index] = number >> 24
    index += 1
    buffer[index] = number >> 16
    index += 1
    buffer[index] = number >> 8
    index += 1
    buffer[index] = number & 0xFF

def comm_can_transmit_eid(id, data, length):
    """Transmit a CAN message with extended ID."""
    msg = can.Message(arbitration_id=id, data=data, is_extended_id=True)
    can0.send(msg)

try:
    # Set up the CAN interface with the specified bitrate
    print("Setting bitrate for can0...")
    os.system('sudo ip link set can0 type can bitrate 1000000')
    print("Bringing can0 interface up...")
    os.system('sudo ip link set can0 up')  # Bring the interface up
    print("can0 interface is up.")

    # Create the CAN bus interface
    print("Initializing CAN bus...")
    can0 = can.interface.Bus(interface='socketcan', channel='can0')
    print("CAN bus initialized successfully.")

    # Create threads for sending and receiving messages
    receiver_thread = threading.Thread(target=receive_can_messages, args=(can0,), daemon=True)

    # Start the receiver thread
    receiver_thread.start()

    # Send commands based on user input
    send_command(can0)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Bring the interface down
    print("Bringing can0 interface down...")
    os.system('sudo ip link set can0 down')
    print("can0 interface is down.")
