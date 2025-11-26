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

        if len(list_n) >= 4:
            list_n.sort()
            return list_n

def IsMoveDone(indy):
    while True:
        status = indy.get_robot_status()
        sleep(0.5)
        if status['movedone'] == True:
            break

def grip(hold, indy):
    indy.set_do(2, hold)

def PickandPlace(indy , list_i, seqnum, seqblock):

    for j in range(len(list_i)):
        seqblock = j
        seqnum = 0
        j_pos_Ab1 = [-44.63, -44.94,-39.79, -14.97,-112.77,-50.14]
        j_pos_Ab2 = [-44.75, -37.67, -74.23, -12.48,-80.36,-0.05]
        t_pos_Ab1 = [ 0.310,  -0.400, 0.463, 0, -180, 0]
        # t_pos_Ab1 = [ 0.30310,  -0.404, 0.44395, 0, 180, 0]
        t_pos_rel1 =  [(-0.04 * int(((list_i[j] - 1) / 5) % 5) ), 0.04 * ((list_i[j] - 1) % 5), 0.04 * ((list_i[j] - 1) // 25), 0, 0, 0]
        res_pos = []
        for i in range(len(t_pos_Ab1 )):
            res_pos.append(t_pos_Ab1 [i] + t_pos_rel1[i])
        t_pos_rel1 = [0, 0, -0.07, 0, 0, 0]
        t_pos_rel2 = [0, 0, +0.07, 0, 0, 0]

        while True:
        
            indy.connect()
            if seqnum == 0 or seqnum == 16:
                indy.go_home()
            elif seqnum == 1 or seqnum == 3 or seqnum == 5 or seqnum == 8 or seqnum == 10 or seqnum == 12 or seqnum == 15 or seqnum == 17:
                IsMoveDone(indy)
            elif seqnum == 2:
                indy.joint_move_to(j_pos_Ab1)
            elif seqnum == 4:
                indy.joint_move_to(j_pos_Ab2)
            elif seqnum == 6:
                grip(True, indy)
                IsMoveDone(indy)
            elif seqnum == 7:
                indy.joint_move_to(j_pos_Ab1)
            elif seqnum == 9:
                indy.task_move_to(res_pos)
            elif seqnum == 11:
                indy.task_move_by(t_pos_rel1)                     
            elif seqnum == 13:
                grip(False, indy)
                IsMoveDone(indy)    
            elif seqnum == 14:    
                indy.task_move_by(t_pos_rel2)
            elif seqnum > 17:
                seqnum = 0
                break
        
            seqnum += 1
            indy.disconnect()

   


robot_ip = "192.168.3.5"  # Robot (Indy) IP
robot_name = "NRMK-Indy7"  # Robot name (Indy7)
# robot_name = "NRMK-IndyRP2"  # Robot name (IndyRP2)

# Create class object
indy1 = client.IndyDCPClient(robot_ip, robot_name)

seqnum = 0
seqblock = 0
list_num = []
PickandPlace(indy1 , inputList(list_num), seqnum, seqblock)
