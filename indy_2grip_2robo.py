from indy_utils import indydcp_client as client

import json
from time import sleep
import threading
import numpy as np

def inputList(list_n):

    while True:
        i = int(input("Place 할 위치 좌표 설정 (1 ~ 25) : "))
        list_n.append(i)
        list_n = set(list_n)
        list_n = list(list_n)

        if len(list_n) >= 1:
            list_n.sort()
            return list_n

def IsMoveDone(indy):
    while True:
        status = indy.get_robot_status()
        sleep(0.5)
        if status['movedone'] == True:
            break

def grip(hold, indy):
    indy.set_do(1, hold)
    indy.set_do(0, not hold)

def PickandPlace(indy, indy1 , list_i, seqnum):
    seqnum = 0
    j_pos_Ab1 = [-44.63, -44.94,-39.79, -14.97,-112.77,-50.14]
    j_pos_Ab2 = [-46.24, -45.06, -79.81, -14.98,-73.53,-127.67]
    j_pos_Ab3 = [-80.24, -27.20, -60.86, 86.38, 10.98, 7.83]

    j2_pos_Ab1 = [85.43, -29.98, -57.16, 90.93, -1.25, 175.70]
    t_pos_Ab1 = [ 0.310,  -0.400, 0.463, 0, -180, 0]

    for j in range(len(list_i)):
        # t_pos_Ab1 = [ 0.30310,  -0.404, 0.44395, 0, 180, 0]
        t_pos_rel =  [(-0.04 * int(((list_i[j] - 1) / 5) % 5) ), 0.04 * ((list_i[j] - 1) % 5), 0.04 * ((list_i[j] - 1) // 25), 0, 0, 0]
        res_pos = []
        for i in range(len(t_pos_Ab1 )):
            res_pos.append(t_pos_Ab1 [i] + t_pos_rel[i])
        t_pos_rel1 = [0, 0, -0.148, 0, 0, 0]
        t_pos_rel2 = [0, 0, +0.148, 0, 0, 0]
        print(f"t_pos_rel1 = {t_pos_rel1}\nt_pos_rel2 = {t_pos_rel2}\n")
        while True:
        
            indy.connect()
            indy1.connect()
            if seqnum == 0 or seqnum == 12:
                indy.go_home()
                indy1.go_home()
            elif seqnum == 1 or seqnum == 3 or seqnum == 5 or seqnum == 8 or seqnum == 10 or seqnum == 13:
                IsMoveDone(indy)
                IsMoveDone(indy1)
            elif seqnum == 2:
                indy.joint_move_to(j_pos_Ab1)
            elif seqnum == 4:
                indy.joint_move_to(j_pos_Ab2)
            elif seqnum == 6:
                grip(True, indy)
                IsMoveDone(indy)
            elif seqnum == 7:
                indy.joint_move_to(j_pos_Ab1)
                indy1.joint_move_to(j2_pos_Ab1)
            elif seqnum == 9:
                indy.joint_move_to(j_pos_Ab3)
            elif seqnum == 11:
                grip(True, indy1)
                grip(False, indy)
                IsMoveDone(indy)
                IsMoveDone(indy1)
            elif seqnum > 13:
                seqnum = 0
                break
        
            seqnum += 1
            indy.disconnect()
            indy1.disconnect()

   


robot_ip1 = "192.168.3.5"  # Robot (Indy) IP
robot_name1 = "NRMK-Indy7"  # Robot name (Indy7)
# robot_name = "NRMK-IndyRP2"  # Robot name (IndyRP2)
robot_ip2 = "192.168.3.6"  # Robot (Indy) IP
robot_name2 = "NRMK-Indy7"  # Robot name (Indy7)
# Create class object
indy1 = client.IndyDCPClient(robot_ip1, robot_name1)
indy2 = client.IndyDCPClient(robot_ip2, robot_name2)

seqnum = 0
list_num = []
status = indy2.get_robot_status()
print(status)
