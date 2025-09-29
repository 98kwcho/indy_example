import csv
from indy_utils import indydcp_client as client

import json
from time import sleep
import threading
import numpy as np

# csv 저장
def file_save(list):
    with open('example.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerows(list)

# csv 읽기
def file_load():
    result = []
    with open('example.csv', 'r', encoding='utf-8-sig') as f:
        rdr = csv.reader(f)
        for line in rdr:
            if len(line) != 1:
                res = (int(line[0]) * 10) + (int(line[1]))
                result.append(res)
            else : 
                res = int(line[0])
                result.append(res)

        f.close()
    return result


def preprocess_list(list_t):
    # 25이상 수는 제거
    for i in list_t:
        if i > 25:
            list_t.remove(i)
    
    for i in range(len(list_t)):
        for j in range(len(list_t)):
            if i != j:
                if list_t[i] == list_t[j]:
                    list_t[j] += 25

def IsMoveDone(indy):
    while True:
        status = indy.get_robot_status()
        sleep(0.5)
        if status['movedone'] == True:
            break

def grip(hold, indy):
    indy.set_do(1, hold)
    indy.set_do(0, not hold)

def PickandPlace(indy , list_i, seqnum):
    seqnum = 0
    j_pos_Ab1 = [-44.63, -44.94,-39.79, -14.97,-112.77,-50.14]
    j_pos_Ab2 = [-46.24, -45.06, -79.81, -14.98,-73.53,-127.67]
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
num = 0

data = ["2", "10", "25", "2"]

res_list = file_load()
preprocess_list(res_list)
PickandPlace(indy1 , res_list, num)

