import numpy as np
import os
import csv
import shutil

VISIBILITY_RANGE = 4
PASSENGER_NUM = 127+18
TOTAL_AISLE_NUM = 127+18 + 4  # 最优 disembarking 策略就是把所有乘客预先排成一列
INFINITY = 99999
NATURAL_VELOCITY = 0.8  # m/s
SEAT_WIDTH = 0.8  # m
SIMULATION_TAU = 1 / 3  # s

f = open('log.txt', 'w')
class passenger:
    def __init__(self, sequence=0, curx=0.00, curcell=0, state=0, velocity=0,waiting_time = 0):
        self.sequence = sequence
        self.curx = curx
        # self.cury = cury
        self.curcell = curcell  # 当前所在过道单元格
        self.state = state
        self.velocity = velocity
        self.waiting_time = waiting_time


passenger_set = [0 for i in range(PASSENGER_NUM)]
position_set = [i - 4 for i in range(TOTAL_AISLE_NUM)]  # 初始化
position_set[0] = position_set[1] = position_set[2] = position_set[3] = INFINITY
finished = []
time_step = 0


def is_anyone_in_the_cell(num):
    if position_set[num] == INFINITY:
        return False
    else:
        return True


def get_current_cell(pasng):
    return np.floor(pasng.curx)


def update_position_set():
    for i in range(TOTAL_AISLE_NUM):
        position_set[i] = INFINITY
    for i in range(PASSENGER_NUM):
        if passenger_set[i].sequence in finished:
            position_set[passenger_set[i].sequence] = INFINITY
            continue
        passenger_set[i].curcell = get_current_cell(passenger_set[i])
        position_set[int(passenger_set[i].curcell)] = passenger_set[i].sequence


def get_visibility(pasng):  # 返回拥堵指数 E.g. 前四格里有两个人，返回 0.5
    cnt = 0  # 前 VISIBILITY_RANGE 里面有多少乘客
    for i in range(int(pasng.curcell - 4), int(pasng.curcell)):
        if is_anyone_in_the_cell(i):
            cnt = cnt + 1
    return (cnt / VISIBILITY_RANGE)


def get_velocity(pasng):
    return NATURAL_VELOCITY * (1 - get_visibility(pasng))


# 排在前面的人编号小
for i in range(PASSENGER_NUM):
    passenger_set[i] = passenger()
    passenger_set[i].sequence = i
    passenger_set[i].curx = i + 4  # 从舱门到后面编号为 0,1,2,……，但第一个乘客并不是在“门”处
    passenger_set[i].curcell = i + 4  # 原因同上
    passenger_set[i].velocity = get_velocity(passenger_set[i])
    passenger_set[i].waiting_time = 0

while len(finished) != PASSENGER_NUM:
    time_step = time_step + 1
    if time_step%50==0:
        f.write(str(finished))
        print(f'time step: {time_step}')
    for i in range(PASSENGER_NUM):
        update_position_set()
        if i not in finished:
            passenger_set[i].velocity = get_velocity(passenger_set[i])
            if passenger_set[i].state == 0:
                passenger_set[i].curx = passenger_set[i].curx - passenger_set[i].velocity * SIMULATION_TAU
                if passenger_set[i].curx<4:
                    finished.append(i)
        else:
            continue


print(time_step)