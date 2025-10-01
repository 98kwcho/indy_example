from indy_utils import indydcp_client as client

import json
from time import sleep
import threading
import numpy as np

def IsMoveDone(indy):
    while True:
        status = indy.get_robot_status()
        sleep(0.5)
        if status['movedone'] == True:
            break

def grip(hold, indy):
    indy.set_do(2, hold)

def PickandPlace(indy, seqnum, pos):
    seqnum = 0
    home_pos = [0.35001, -0.18648, 0.52194, 0, -180, 0]
    app_t_pos_by = []
    for i in range(len(home_pos)):
        app_t_pos_by.append(pos[i] - home_pos[i])    
    tar_t_pos_by = [0, 0, 0, 0, 0, 0]
    tar_t_pos_by[2] = -(0.42317 - 0.27444)	
    ret_t_pos_by = [0, 0, 0, 0, 0, 0]
    ret_t_pos_by[2] = -tar_t_pos_by[2]
    ret_t_pos_by[5] = -app_t_pos_by[5]

    print(app_t_pos_by)
    print(tar_t_pos_by)
    print(ret_t_pos_by)
    app_t_sup_to = [0.01512, -0.57770, 0.50624, -1.99, -160.93, 0.85]
    tar_t_sup_to = [-0.01028, -0.57542, 0.43172, -1.96, -160.99, 0.92]

    while True:       
        indy.connect()
        if seqnum == 0:
            indy.go_home()
            IsMoveDone(indy)
        elif seqnum == 1:
            indy.task_move_by(app_t_pos_by)
            IsMoveDone(indy)
            print("app")
        elif seqnum == 2:
            indy.task_move_by(tar_t_pos_by)
            IsMoveDone(indy)
            print("tar")           
        elif seqnum == 3:
            grip(True, indy)
            IsMoveDone(indy)
        elif seqnum == 4:
            indy.task_move_by(ret_t_pos_by)
            IsMoveDone(indy)
            print("ret")            
        elif seqnum == 5:
            indy.go_home()
            IsMoveDone(indy)
        elif seqnum == 6:
            indy.task_move_to(app_t_sup_to)
            IsMoveDone(indy)
        elif seqnum == 7:
            indy.task_move_to(tar_t_sup_to)
            IsMoveDone(indy)
        elif seqnum == 8:
            grip(False, indy)
            IsMoveDone(indy)      
        elif seqnum == 9:
            indy.task_move_to(app_t_sup_to)
            IsMoveDone(indy)
        elif seqnum == 10:
            indy.go_home()
            IsMoveDone(indy)     
            break   
        seqnum += 1
        indy.disconnect()


robot_ip = "192.168.3.5"  # Robot (Indy) IP
robot_name = "NRMK-Indy7"  # Robot name (Indy7)
# robot_name = "NRMK-IndyRP2"  # Robot name (IndyRP2)

# Create class object
indy1 = client.IndyDCPClient(robot_ip, robot_name)

seqnum = 0

pos = [0.39421, -0.13989, 0.42317, 0, -180, 30]
PickandPlace(indy1, seqnum, pos)
