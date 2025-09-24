from indy_utils import indydcp_client as client

import json
from time import sleep
import threading
import numpy as np

def IsMoveDone(indy_t):
    while True:
        status = indy_t.get_robot_status()
        sleep(0.5)
        if status['movedone'] == True:
            break

def grip(hold, indy_t):
    indy_t.set_do(2, hold)

def DrawSquare_Tmoveby(seqnum, indy_t):
    seqnum = 0
    input_lenght = int(input("사각형의 길이를 설정하세요. 단위 : mm :"))
    input_lenght = input_lenght / 1000

    while True:
        #logical / calc
        t_pos_edge2 = [0, -input_lenght, 0, 0, 0, 0]
        t_pos_edge3 = [-input_lenght ,0, 0, 0, 0, 0]
        t_pos_edge4 = [0, +input_lenght, 0, 0, 0, 0]
        t_pos_edge5 = [+input_lenght ,0, 0, 0, 0, 0]

        # indy / comm/ working
        indy_t.connect()
        if seqnum == 0:
            indy_t.go_home()
        elif seqnum == 2:
            indy_t.task_move_by(t_pos_edge2)
        elif seqnum == 4:
            indy_t.task_move_by(t_pos_edge3)
        elif seqnum == 6:
            indy_t.task_move_by(t_pos_edge4)
        elif seqnum == 8:
            indy_t.task_move_by(t_pos_edge5)
        elif seqnum == 1 or seqnum == 3 or seqnum == 5 or seqnum == 7 or seqnum == 9:
            IsMoveDone(indy_t)
        elif seqnum > 9:
            indy_t.go_home()
            seqnum = 0
            break

        seqnum += 1
        indy_t.disconnect()



robot1_ip = "192.168.3.5"  # Robot (Indy) IP
robot1_name = "NRMK-Indy7"  # Robot name (Indy7)
# robot_name = "NRMK-IndyRP2"  # Robot name (IndyRP2)

robot2_ip = "192.168.3.6"  # Robot (Indy) IP
robot2_name = "NRMK-Indy7"  # Robot name (Indy7)

robot3_ip = "192.168.3.7"  # Robot (Indy) IP
robot3_name = "NRMK-Indy7"  # Robot name (Indy7)

# Create class object
indy1 = client.IndyDCPClient(robot1_ip, robot1_name)
indy2 = client.IndyDCPClient(robot2_ip, robot2_name)
indy3 = client.IndyDCPClient(robot3_ip, robot3_name)
cnt = 0

DrawSquare_Tmoveby(cnt, indy1)
DrawSquare_Tmoveby(cnt, indy2)
DrawSquare_Tmoveby(cnt, indy3)