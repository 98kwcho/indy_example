from indy_utils import indydcp_client as client
from testPLC import str_to_word

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

# AI 모델에서 출력된 BBox를 이용하여 CV의 PCA 알고리즘을 이용한 회전값 계산 (OBB 오브젝트 디텍션이 실패할 경우 사용할 함수)
def PCA_BBox(bbox_pos):
    theta = bbox_pos
    return theta

# 카메라 포지션에서 로봇 포지션으로 변환 해주는 함수
def cvTorobot(pos):
    res_pos = pos
    return res_pos

# 키켑의 회전량(theta)값을 계산하여 정위치를 robot이 pick & place하는 함수
def keycap_pickandplace(indy_t, theta):
    return

# 키켑의 양품 불량품을 구분해 robot이 불량품을 배출하는 함수
def classify_product(indy_t):
    return

# 함수들을 총 집합 시킨 매인 함수
def main_function(indy_t):
    pass

robot_ip = "192.168.3.5"  # Robot (Indy) IP
robot_name = "NRMK-Indy7"  # Robot name (Indy7)
# robot_name = "NRMK-IndyRP2"  # Robot name (IndyRP2)

# Create class object
indy1 = client.IndyDCPClient(robot_ip, robot_name)

main_function(indy1)
