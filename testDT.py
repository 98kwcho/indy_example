from indy_utils import indydcp_client as client

import json
from time import sleep
import threading
import numpy as np
import cv2


# Model = 사용할 AI 모델

# robot의 동작이 끝났는가를 체크하는 함수
def IsMoveDone(indy_t):
    while True:
        status = indy_t.get_robot_status()
        sleep(0.5)
        if status['movedone'] == True:
            break

# robot 엔드 툴 동작 함수(엔드 툴의 증감에 따라 변경 또는 추가가 이루어질 수 있음)
def grip(hold, indy_t):
    indy_t.set_do(2, hold)

# 카메라를 통해 로봇이 pick & place 해야할 오브젝트의 좌표를 잡는다.
def camDetect(frame):
    # YOLO 결과라고 가정 (예시값)
    box_x, box_y, box_w_px, box_h_px = 400, 200, 300, 530   # 박스 위치
    obj_x, obj_y, obj_w, obj_h = 450, 300, 80, 100          # 오브젝트 bbox

    # 물체 중심(영상 전체 기준)
    cx_global = obj_x + obj_w / 2
    cy_global = obj_y + obj_h / 2

    # 1) 박스 내부 좌표로 변환
    cx_local = cx_global - box_x
    cy_local = cy_global - box_y

    # 2) 좌측 하단 원점 좌표로 변환
    cx_bottom = cx_local
    cy_bottom = box_h_px - cy_local

    # 실제 박스 크기(cm → m)
    BOX_W = 0.085       # 8.5 cm
    BOX_H = 0.150       # 15 cm

    # 픽셀 → 미터 변환 비율
    cm_per_px_x = BOX_W / box_w_px
    cm_per_px_y = BOX_H / box_h_px

    # 최종 좌표 (박스 좌측 하단 기준, 미터)
    px = cx_bottom * cm_per_px_x
    py = cy_bottom * cm_per_px_y

    return [px, py]

# 카메라 좌표에서 로봇좌표로 변환하는 함수
def conCamtoRobo(cam_point):
    px, py = cam_point  # meters, 박스 좌하단 기준

    # 박스의 좌측 하단 (0,0) 실제 로봇 좌표
    zero_x = 0.50790
    zero_y = -0.02140
    zero_z = 0.500

    # 카메라 좌표 → 로봇 좌표 매핑
    robot_x = zero_x + px
    robot_y = zero_y + py
    robot_z = zero_z

    # 자세(오리엔테이션) 고정
    roll, pitch, yaw = -180, 0, 180

    return [robot_x, robot_y, robot_z, roll, pitch, yaw]


# 로봇으로 오브젝트를 pick & place를 하는 함수
def picknPlace(indy_t, conRobo, seqnum):

    # 오브젝트를 담고 있는 상자의 좌측 하단 모서리의 좌표를 0, 0으로 잡는다.
    zero = [0.50790, -0.02140, 0.500, -180, 0, 180]

    # 타겟의 좌표 수정
    app = conRobo.copy()
    target = conRobo.copy()

    app[2] == 0.500

    # 상자의 너비, 높이
    width = 0.085
    height = 0.15

    # 실제 로봇 동작
    while(True):
        indy_t.connect()    
        if seqnum == 0:
            indy_t.go_home()

        elif seqnum == 2:
            indy_t.task_move_to(zero)
        elif seqnum == 4:
            indy_t.task_move_to(app)

        elif seqnum == 1 or seqnum == 3 or seqnum == 5: 
            IsMoveDone(indy_t)

        seqnum += 1
        indy_t.disconnect()


# 함수들을 총 집합 시킨 매인 함수
def main_function(indy_t):
    pass

robot_ip = "192.168.3.6"  # Robot (Indy) IP
robot_name = "NRMK-Indy7"  # Robot name (Indy7)
# robot_name = "NRMK-IndyRP2"  # Robot name (IndyRP2)

# Create class object
indy1 = client.IndyDCPClient(robot_ip, robot_name)

main_function(indy1)
