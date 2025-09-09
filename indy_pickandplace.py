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

robot_ip = "192.168.3.5"  # Robot (Indy) IP
robot_name = "NRMK-Indy7"  # Robot name (Indy7)
# robot_name = "NRMK-IndyRP2"  # Robot name (IndyRP2)

# Create class object
indy = client.IndyDCPClient(robot_ip, robot_name)

indy.connect()

status = indy.get_robot_status()
j_pos1 = indy.get_joint_pos()
t_pos1 = indy.get_task_pos()
print("j_pos1", j_pos1)
print("t_pos1", t_pos1)

indy.go_home()
IsMoveDone()

j_pos_rel = [-31, -17, -76, 0, -87, -32]
indy.joint_move_to(j_pos_rel)
IsMoveDone()

t_pos_rel = [0, 0, -0.07, 0, 0, 0]
indy.task_move_by(t_pos_rel)
IsMoveDone()
grip(True)

t_pos_rel = [0, 0, +0.07, 0, 0, 0]
indy.task_move_by(t_pos_rel)
IsMoveDone()

t_pos_rel = [0, 0.082, 0, 0, 0, 0]
indy.task_move_by(t_pos_rel)
IsMoveDone()

t_pos_rel = [0, 0, -0.07, 0, 0, 0]
indy.task_move_by(t_pos_rel)
IsMoveDone()
grip(False)

t_pos_rel = [0, 0, +0.07, 0, 0, 0]
indy.task_move_by(t_pos_rel)
IsMoveDone()

indy.go_home()
IsMoveDone()

print("j_pos1", j_pos1)
print("t_pos1", t_pos1)

indy.disconnect()