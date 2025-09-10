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

def DrawSquare_Jmoveto():
    j_pos_edge1 = [-31, -18, -74, 0, -90, 0]
    indy.joint_move_to(j_pos_edge1)
    IsMoveDone()

    j_pos_edge2 = [-10, -2, -94, 1, -87, 21]
    indy.joint_move_to(j_pos_edge2)
    IsMoveDone()

    j_pos_edge3 = [-18, 17, -110, 0, -90, 13]
    indy.joint_move_to(j_pos_edge3)
    IsMoveDone()

    j_pos_edge4 = [-46, -7, -89, -1, -87, -15]
    indy.joint_move_to(j_pos_edge4)
    IsMoveDone()

    j_pos_edge5 = [-31, -18, -74, 0, -90, 0]
    indy.joint_move_to(j_pos_edge5)
    IsMoveDone()

def DrawSquare_Jmoveby():
    j_pos_edge1 = [-31, -18, -74, 0, -90, 0]
    indy.joint_move_to(j_pos_edge1)
    IsMoveDone()

    j_pos_edge2 = [21, 16, -20, 1, 3, 21]
    indy.joint_move_by(j_pos_edge2)
    IsMoveDone()

    j_pos_edge3 = [-8, 19, -16, -1, -3, -8]
    indy.joint_move_by(j_pos_edge3)
    IsMoveDone()

    j_pos_edge4 = [-28, -24, 21, -1, 3, -28]
    indy.joint_move_by(j_pos_edge4)
    IsMoveDone()

    j_pos_edge5 = [5, -11, 15, 1, -3, 15]
    indy.joint_move_by(j_pos_edge5)
    IsMoveDone()

def DrawSquare_Tmoveto():
    t_pos_edge1 = [0.316, -0.407, 0.487, 180, -2, 150]
    indy.task_move_to(t_pos_edge1)
    IsMoveDone()

    t_pos_edge2 = [0.316, -0.240, 0.487, 180, -2, 150]
    indy.task_move_to(t_pos_edge2)
    IsMoveDone()

    t_pos_edge3= [0.138, -0.240, 0.487, 180, -2, 150]
    indy.task_move_to(t_pos_edge3)
    IsMoveDone()

    t_pos_edge4= [0.138, -0.407, 0.487, 180, -2, 150]
    indy.task_move_to(t_pos_edge4)
    IsMoveDone()

    t_pos_edge5= [0.316, -0.407, 0.487, 180, -2, 150]
    indy.task_move_to(t_pos_edge5)
    IsMoveDone()

def DrawSquare_Tmoveby():
    input_lenght = int(input("사각형의 길이를 설정하세요. 단위 : mm :"))
    input_lenght = input_lenght / 1000
    
    t_pos_edge1 = [0.316, -0.407, 0.487, 180, -2, 150]
    indy.task_move_to(t_pos_edge1)
    IsMoveDone()

    t_pos_edge2 = [0, -input_lenght, 0, 0, 0, 0]
    print(t_pos_edge2)
    indy.task_move_by(t_pos_edge2)
    IsMoveDone()

    t_pos_edge3 = [-input_lenght ,0, 0, 0, 0, 0]
    indy.task_move_by(t_pos_edge3)
    IsMoveDone()

    t_pos_edge4 = [0, +input_lenght, 0, 0, 0, 0]
    indy.task_move_by(t_pos_edge4)
    IsMoveDone()

    t_pos_edge5 = [input_lenght ,0, 0, 0, 0, 0]
    indy.task_move_by(t_pos_edge5)
    IsMoveDone()



robot_ip = "192.168.3.5"  # Robot (Indy) IP
robot_name = "NRMK-Indy7"  # Robot name (Indy7)
# robot_name = "NRMK-IndyRP2"  # Robot name (IndyRP2)

# Create class object
indy = client.IndyDCPClient(robot_ip, robot_name)

while True:
    input_num = int(input("타입 설정 (1 ~ 4) : " ))
    if input_num > 0 and input_num  < 5:
        break

indy.connect()
j_pos1 = indy.get_joint_pos()
t_pos1 = indy.get_task_pos()



indy.go_home()
IsMoveDone()

if input_num == 1:
    DrawSquare_Jmoveto()
elif input_num == 2:
    DrawSquare_Jmoveby()
elif input_num == 3:
    DrawSquare_Tmoveto()
elif input_num == 4:
    DrawSquare_Tmoveby()

indy.go_home()
IsMoveDone()
indy.disconnect()