from indy_utils import indydcp_client as client

import json
from time import sleep
import threading
import numpy as np
import math

def IsMoveDone():
    while True:
        status = indy.get_robot_status()
        sleep(0.5)
        if status['movedone'] == True:
            break

def MoveFunc(DTList):
    for i in range(len(DTList)):
        for j in range(len(DTList[i])):
            if j < 3:
                DTList[i][j] = DTList[i][j] / 100000

        #print(DTList[i])
        indy.task_move_to(DTList[i])
        IsMoveDone()

robot_ip = "192.168.3.5"  # Robot (Indy) IP
robot_name = "NRMK-Indy7"  # Robot name (Indy7)
# robot_name = "NRMK-IndyRP2"  # Robot name (IndyRP2)

# Create class object
indy = client.IndyDCPClient(robot_ip, robot_name)

DTJList = []
DTTList = []
count = 0
listCount = 0
lastJPos = [0,0,0,0,0,0]
lastTPos = [0,0,0,0,0,0]

indy.connect()

indy.direct_teaching(True)

while count < 3:
    sleep(1)
    currTPos = indy.get_task_pos()

    for i in range(len(currTPos)):

        if i < 3:
            currTPos[i] = math.trunc(currTPos[i] * 100000)

        else:
            currTPos[i] = math.trunc(currTPos[i])

    if lastTPos == currTPos:
        count = count + 1
        print(f"{count}초 경과")
    
    else : 
        DTTList.append(currTPos)
        listCount = listCount + 1
        count = 0

    lastTPos = currTPos

indy.direct_teaching(False)

indy.go_home()
IsMoveDone()

MoveFunc(DTTList)

indy.go_home()
IsMoveDone()

indy.disconnect()