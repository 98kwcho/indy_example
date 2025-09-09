from indy_utils import indydcp_client as client

import json
from time import sleep
import threading
import numpy as np

def IsMoveDone():
    while True:
        status = indy.get_robot_status()
        sleep(0.5)
        if status['movedone'] == True:
            break

def grip(hold):
    indy.set_do(2, hold)


def Place():
    t_pos_rel1 = [0, 0, -0.07, 0, 0, 0]
    indy.task_move_by(t_pos_rel1)
    IsMoveDone()
    grip(False)
    IsMoveDone()
    t_pos_rel2 = [0, 0, +0.07, 0, 0, 0]
    indy.task_move_by(t_pos_rel2)
    IsMoveDone()


robot_ip = "192.168.3.5"  # Robot (Indy) IP
robot_name = "NRMK-Indy7"  # Robot name (Indy7)
# robot_name = "NRMK-IndyRP2"  # Robot name (IndyRP2)

# Create class object
indy = client.IndyDCPClient(robot_ip, robot_name)

indy.connect()

status = indy.get_robot_status()
j_pos1 = indy.get_joint_pos()
t_pos1 = indy.get_task_pos()

i = int(input("Place 할 위치 좌표 설정 (1 ~ 25) : "))

indy.go_home()
IsMoveDone()

j_pos_Ab1 = [-44.63, -44.94,-39.79, -14.97,-112.77,-50.14]
indy.joint_move_to(j_pos_Ab1)
IsMoveDone()

j_pos_Ab2 = [-44.75, -37.67, -74.23, -12.48,-80.36,-0.05]
indy.joint_move_to(j_pos_Ab2)
IsMoveDone()
grip(True)
IsMoveDone()

indy.joint_move_to(j_pos_Ab1)
IsMoveDone()

t_pos_Ab1 = [ 0.310,  -0.400, 0.430, 0, -180, 0]

'''
for i in range(25): 
    t_pos_rel1 =  [(-0.04 * int((i) / 5)), 0.04 * ((i) % 5), 0, 0, 0, 0]
    res_pos = []
    for j in range(6):
        res_pos.append(t_pos_Ab1 [j] + t_pos_rel1[j])

    print(i, res_pos)
#    indy.task_move_to(res_pos)
#    IsMoveDone()
'''
t_pos_Ab1 = [ 0.310,  -0.400, 0.463, 0, -180, 0]
# t_pos_Ab1 = [ 0.30310,  -0.404, 0.44395, 0, 180, 0]
t_pos_rel1 =  [(-0.04 * int((i - 1) / 5)), 0.04 * ((i - 1) % 5), 0, 0, 0, 0]

res_pos = []
for i in range(len(t_pos_Ab1 )):
    res_pos.append(t_pos_Ab1 [i] + t_pos_rel1[i])

indy.task_move_to(res_pos)
IsMoveDone()
Place()


indy.go_home()
IsMoveDone()

indy.disconnect()