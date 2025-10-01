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

def PickandPlace(indy , inputNum, seqnum):
    flg = True
    num = inputNum / 1000
    seqnum = 0
    j_pos_Ab1 = [69.28, -33.70, -43.49, 22.74, -110.57, 76.01]
    j_pos_Ab2 = [74.56, -32.20, -68.23, 22.05, -86.96, 72.08]
    t_pos_Ab1 = [0.26450, 0.40808, 0.48780, -180, 0, 180]

    for j in range(4):
        # t_pos_Ab1 = [ 0.30310,  -0.404, 0.44395, 0, 180, 0]
        t_pos_rel =  [(-num * (j // 2)), (-num *(j % 2)), 0 , 0, 0, 0]
        res_pos = []
        for i in range(len(t_pos_Ab1 )):
            res_pos.append(t_pos_Ab1 [i] + t_pos_rel[i])
        t_pos_rel1 = [0, 0, -0.07, 0, 0, 0]
        t_pos_rel2 = [0, 0, +0.07, 0, 0, 0]

        indy.connect()
        dis = indy.get_di()
        if dis[3] : 
            flg = True
        else :
            flg = False
        indy.disconnect()

        while not flg:
            indy.connect()
            dis = indy.get_di()
            if dis[3] : 
                flg = True
                break
            indy.disconnect()
            print("조건을 기다리는 중...")
            sleep(1)

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

   


robot_ip = "192.168.3.3"  # Robot (Indy) IP
robot_name = "NRMK-Indy7"  # Robot name (Indy7)
# robot_name = "NRMK-IndyRP2"  # Robot name (IndyRP2)

# Create class object
indy1 = client.IndyDCPClient(robot_ip, robot_name)

seqnum = 0
inputNum = int(input("길이 입력(40 ~ 120) : "))

PickandPlace(indy1 , inputNum, seqnum)
