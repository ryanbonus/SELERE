import numpy as np
from kneeMotor.motorCAN import comm_can_transmit_eid

#Motor parameters
BITRATE = 500000
CONTROLLER_ID = 0

# CAN packet definitions
CAN_PACKET_SET_DUTY = 0
CAN_PACKET_SET_CURRENT = 1
CAN_PACKET_SET_CURRENT_BRAKE = 2
CAN_PACKET_SET_RPM = 3
CAN_PACKET_SET_POS = 4
CAN_PACKET_SET_ORIGIN_HERE = 5
CAN_PACKET_SET_POS_SPD = 6


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

def position_speed_acceleration(bus, position, speed, rpa, controller_id=CONTROLLER_ID):
    position_index = 0
    speed_index = 4
    rpa_index = 6
    buffer = bytearray(0)
    buffer_append_int32(buffer, np.int32(position*10000), position_index)
    buffer_append_int16(buffer, speed/10, speed_index)
    buffer_append_int16(buffer, rpa/10, rpa_index)
    eid = (controller_id | int(CAN_PACKET_SET_POS_SPD) << 8)
    comm_can_transmit_eid(bus, eid, buffer)

def current(bus, current, controller_id=CONTROLLER_ID):
    current_index = 0
    buffer = bytearray(0)
    buffer_append_int32(buffer, np.int32(current*1000), current_index)
    eid = (controller_id | int(CAN_PACKET_SET_CURRENT) << 8)
    comm_can_transmit_eid(bus, eid, buffer)   

def current_brake(bus, current, controller_id=CONTROLLER_ID):
    current_index = 0
    buffer = bytearray(0)
    buffer_append_int32(buffer, np.int32(current*1000), current_index)
    eid = (controller_id | int(CAN_PACKET_SET_CURRENT_BRAKE) << 8)
    comm_can_transmit_eid(bus, eid, buffer)

    def set_origin(controller_id: int, set_origin_mode: int):
        mode_index = 0
        buffer = bytearray(0)
        buffer_append(1, buffer, set_origin_mode, mode_index)
        eid = (controller_id | int(CAN_PACKET_SET_ORIGIN_HERE) << 8)
        comm_can_transmit_eid(bus, eid, buffer)  