import numpy as np
import os
import csv
import shutil

f = open('log.txt', 'w')


class passenger:
    def __init__(self, target_x=0, target_y=0, curx=0.00, cury=0.00, sequence=0, state=0, velocity=0,
                 density=0, luggage_time_left=0, waiting_time_left=0, aisle_state=0, target_block=0):
        self.target_x = target_x  # 所在座位的行数，从前到后编号为 1,2,……
        self.target_y = target_y  # 所在座位的列数
        self.curx = curx
        self.cury = cury
        self.sequence = sequence  # 排队的顺序
        self.state = state  # 0=在走路, 1=停止但没到, 2=停止且到了, 3=坐好了
        self.velocity = velocity
        self.density = density
        self.luggage_time_left = luggage_time_left  # 放行李还剩多少时间
        self.waiting_time_left = waiting_time_left  # 还要等多久
        self.aisle_state = aisle_state  # 0=主过道，1=块过道1，……4=块过道4
        self.target_block = target_block  # 1，2，3，4

    def show(self):
        f.write(
            f'()()()()\n'
            f'target_x: {self.target_x}\n'
            f'target_y: {self.target_y}\n'
            f'curx: {self.curx}\n'
            f'cury: {self.cury}\n'
            f'sequence: {self.sequence}\n'
            f'state: {self.state}\n'
            f'velocity: {self.velocity}\n'
            f'aisle_state: {self.aisle_state}\n'
            f'target_block: {self.target_block}\n'
            f'is at block: {is_at_block(self)}\n'
            f'()()()()()()()()')


# class cell:
#     def __init__(self,state = 0,index = 0):
#         self.state = 0 # 0代表主
VISIBILITY_RANGE = 4
PASSENGER_NUM = 318
TOTAL_AISLE_NUM = 1000
INFINITY = 99999
NATURAL_VELOCITY = 0.8  # m/s
SEAT_WIDTH = 0.8  # m
SIMULATION_TAU = 1 / 3  # s
STANDARD_SEATING_TIME = 1  # s ,乘客横向移动一格需要的时间
STANDARD_LUGGAGE_TIME = 5  # s

BLOCK_AISLE_LENGTH = 15  # 同时考虑过道上的那个格
MAIN_AISLE_LENGTH = 1000  # 主过道预留足够空间


def get_block(y):  # 懒得写太多条件了，请确保输入没问题就行
    if y >= 1 and y <= 7:
        return 1
    elif y >= 8 and y <= 14:
        return 2
    elif y >= 15 and y <= 21:
        return 3
    else:
        return 4


passenger_set = [0 for i in range(PASSENGER_NUM)]

targx = [14, 14, 14, 12, 12, 12, 10, 10, 10, 8, 8, 8, 6, 6, 6, 4, 4, 4, 2, 2, 2, 14, 14, 14, 12, 12, 12, 10, 10, 10, 8,
         8, 8, 6, 6, 6, 14, 14, 14, 4, 4, 4, 14, 14, 14, 12, 12, 12, 10, 10, 10, 8, 8, 8, 6, 6, 6, 4, 4, 4, 2, 2, 12,
         14, 14, 14, 12, 12, 12, 10, 10, 10, 8, 8, 8, 6, 6, 6, 4, 2, 2, 12, 4, 2, 14, 12, 4, 2, 14, 10, 2, 14, 14, 10,
         2, 14, 12, 10, 2, 14, 12, 8, 14, 12, 12, 8, 14, 12, 10, 8, 14, 12, 10, 6, 12, 10, 10, 6, 12, 10, 8, 6, 12, 10,
         8, 4, 10, 8, 8, 4, 10, 8, 6, 4, 10, 8, 6, 13, 8, 6, 6, 13, 8, 6, 4, 13, 8, 6, 4, 11, 6, 4, 4, 11, 6, 4, 2, 11,
         6, 4, 2, 9, 4, 2, 2, 9, 4, 2, 13, 9, 4, 2, 13, 7, 13, 13, 13, 7, 13, 13, 11, 7, 13, 13, 11, 5, 11, 11, 11, 5,
         11, 11, 9, 5, 11, 11, 9, 3, 9, 9, 9, 3, 9, 9, 7, 3, 9, 9, 7, 1, 7, 7, 7, 1, 7, 7, 5, 1, 7, 7, 5, 13, 5, 5, 5,
         13, 5, 5, 3, 13, 5, 5, 3, 11, 3, 3, 3, 11, 3, 3, 1, 11, 3, 3, 1, 9, 1, 1, 1, 9, 1, 1, 13, 9, 1, 1, 13, 7, 13,
         13, 13, 7, 13, 13, 11, 7, 13, 13, 11, 5, 11, 11, 11, 5, 11, 11, 9, 5, 11, 11, 9, 9, 9, 9, 9, 9, 7, 9, 9, 7, 7,
         7, 7, 7, 7, 5, 7, 7, 5, 5, 5, 5, 5, 5, 3, 5, 5, 3, 3, 3, 3, 1, 3, 1, 1, 1, 1, 1]
targy = [22, 23, 24, 22, 23, 24, 22, 23, 24, 22, 23, 24, 22, 23, 24, 22, 23, 24, 22, 23, 24, 15, 16, 17, 15, 16, 17, 15,
         16, 17, 15, 16, 17, 15, 16, 17, 28, 27, 26, 15, 16, 17, 14, 13, 12, 14, 13, 12, 14, 13, 12, 14, 13, 12, 14, 13,
         12, 14, 13, 12, 15, 16, 28, 7, 6, 5, 7, 6, 5, 7, 6, 5, 7, 6, 5, 7, 6, 5, 7, 14, 17, 27, 6, 13, 21, 26, 5, 12,
         20, 28, 7, 8, 19, 27, 6, 9, 21, 26, 5, 10, 20, 28, 1, 8, 19, 27, 2, 9, 21, 26, 3, 10, 20, 28, 1, 8, 19, 27, 2,
         9, 21, 26, 3, 10, 20, 28, 1, 8, 19, 27, 2, 9, 21, 26, 3, 10, 20, 22, 1, 8, 19, 23, 2, 9, 21, 24, 3, 10, 20, 22,
         1, 8, 19, 23, 2, 9, 21, 24, 3, 10, 20, 22, 1, 8, 19, 23, 2, 9, 15, 24, 3, 10, 16, 22, 7, 14, 17, 23, 6, 13, 15,
         24, 5, 12, 16, 22, 7, 14, 17, 23, 6, 13, 15, 24, 5, 12, 16, 22, 7, 14, 17, 23, 6, 13, 15, 24, 5, 12, 16, 22, 7,
         14, 17, 23, 6, 13, 15, 24, 5, 12, 16, 28, 7, 14, 17, 27, 6, 13, 15, 26, 5, 12, 16, 28, 7, 14, 17, 27, 6, 13,
         15, 26, 5, 12, 16, 28, 7, 14, 17, 27, 6, 13, 21, 26, 5, 12, 20, 28, 1, 8, 19, 27, 2, 9, 21, 26, 3, 10, 20, 28,
         1, 8, 19, 27, 2, 9, 21, 26, 3, 10, 20, 1, 8, 19, 2, 9, 21, 3, 10, 20, 1, 8, 19, 2, 9, 21, 3, 10, 20, 1, 8, 19,
         2, 9, 21, 3, 10, 20, 8, 19, 9, 21, 10, 20, 8, 19, 9, 10]

main_position_set = [0 for i in range(MAIN_AISLE_LENGTH)]
block_position_set = [0, 0, 0, 0, 0]
for i in range(5):
    block_position_set[i] = [0 for i in range(BLOCK_AISLE_LENGTH)]


def is_anyone_in_main_cell(num):
    if main_position_set[num] == INFINITY:
        return False
    else:
        return True


def is_anyone_in_block_cell(bl, num):
    if block_position_set[bl][num] == INFINITY:
        return False
    else:
        return True


def get_current_cellstate(pasng):
    if pasng.curx == 0:
        return 0
    elif pasng.cury >= 3.5 and pasng.cury <= 4.5:
        return 1
    elif pasng.cury >= 10.5 and pasng.cury <= 11.5:
        return 2
    elif pasng.cury >= 17.5 and pasng.cury <= 18.5:
        return 3
    elif pasng.cury >= 24.5 and pasng.cury <= 25.5:
        return 4


def get_main_cell(pasng):
    ans = int(25 - pasng.cury + 0.5)
    return ans


def get_block_cell(pasng):
    ans = int(pasng.curx + 0.5)
    return ans


def update_position_set():
    for i in range(5):
        for j in range(BLOCK_AISLE_LENGTH):
            block_position_set[i][j] = INFINITY
    for i in range(MAIN_AISLE_LENGTH):
        main_position_set[i] = INFINITY
    for i in range(PASSENGER_NUM):
        if i in finished:
            if passenger_set[i].aisle_state == 0:
                # print('###################')
                main_position_set[get_main_cell(passenger_set[i])] = INFINITY
            else:
                # print('**********************')
                block_position_set[passenger_set[i].aisle_state][get_block_cell(passenger_set[i])] = INFINITY
        if passenger_set[i].aisle_state == 0:
            # print('^^^^^^^^^^^^^^^^^^^^')
            main_position_set[get_main_cell(passenger_set[i])] = passenger_set[i].sequence
        elif passenger_set[i].aisle_state != 0:
            # print('&&&&&&&&&&&&&&&&&&&')
            # print(i)
            # passenger_set[i].show()
            # print(passenger_set[i].aisle_state)
            # print(get_block_cell(passenger_set[i]))
            block_position_set[passenger_set[i].aisle_state][get_block_cell(passenger_set[i])] = i


def get_visibility(pasng):
    cnt = 0
    if pasng.aisle_state == 0:
        for i in range(get_main_cell(pasng) - 4, get_main_cell(pasng)):
            if i < 0:
                continue
            if is_anyone_in_main_cell(i):
                cnt = cnt + 1
    else:
        bl = pasng.aisle_state
        for i in range(get_block_cell(pasng) + 1, get_block_cell(pasng) + 5):
            if i >= 13:
                continue
            else:
                if is_anyone_in_block_cell(bl, i):
                    cnt = cnt + 1
    return (cnt / VISIBILITY_RANGE)


def get_velocity(pasng):
    return NATURAL_VELOCITY * (1 - get_visibility(pasng))


def is_at_block(pasng):
    if pasng.aisle_state == 0 and pasng.cury >= 7 * pasng.target_block - 3.5 and pasng.cury <= 7 * pasng.target_block - 2.5:
        return True
    else:
        return False


def is_at_target(pasng):
    if pasng.aisle_state == pasng.target_block and int(pasng.curx + 0.5) == pasng.target_x:
        return True
    else:
        return False


def get_cells_right_behind(pasng):  # 此时默认pasng已经进入过道
    ans = []
    bl = pasng.target_block
    arr = block_position_set[bl]
    for i in range(get_block_cell(pasng)):
        if is_anyone_in_block_cell(pasng.target_block, i):
            ans.append(arr[i])
    if arr[0] in ans:  # 波及到主过道
        for i in range(7 * (bl - 1) + 1, 600):
            if is_anyone_in_main_cell(i):
                ans.append(main_position_set[i])
    return ans


def put_luggage(pasng):
    pasng.state = 2
    pasng.luggage_time_left = STANDARD_LUGGAGE_TIME
    for j in get_cells_right_behind(pasng):
        if not is_at_target(passenger_set[j]):
            passenger_set[j].state = 1
            passenger_set[j].waiting_time_left = pasng.luggage_time_left
        else:
            passenger_set[j].state = 2


finished = []
for i in range(PASSENGER_NUM):
    passenger_set[i] = passenger()
    passenger_set[i].target_x = targx[i]
    passenger_set[i].target_y = targy[i]
    passenger_set[i].sequence = i  # 0代表最前面那个人
    passenger_set[i].cury = 0 - passenger_set[i].sequence
    passenger_set[i].curx = 0
    passenger_set[i].state = 0
    passenger_set[i].aisle_state = 0
    passenger_set[i].target_block = get_block(passenger_set[i].target_y)
    passenger_set[i].velocity = get_velocity(passenger_set[i])
    passenger_set[i].luggage_time_left = 0
    passenger_set[i].waiting_time_left = 0


def get_blockk_velocity(pasng):
    cnt = 0
    bl = passenger_set[i].target_block
    for i in range(get_block_cell(pasng) + 1, max(get_block_cell(pasng), BLOCK_AISLE_LENGTH - 1)):
        if is_anyone_in_block_cell(bl, i):
            cnt = cnt + 1
    return NATURAL_VELOCITY * (1 - (cnt / VISIBILITY_RANGE))


time_step = 0
while len(finished) != PASSENGER_NUM:
    time_step = time_step + 1
    if time_step % 100 == 0:
        print(finished)
    for i in range(PASSENGER_NUM):
        update_position_set()
        if i == 0:
            passenger_set[i].show()
        if i not in finished:
            passenger_set[i].velocity = get_velocity(passenger_set[i])
            if passenger_set[i].state == 0:
                if passenger_set[i].aisle_state == 0:
                    passenger_set[i].cury = passenger_set[i].cury + passenger_set[i].velocity * SIMULATION_TAU
                    # passenger_set[i].cury = passenger_set[i].cury-0.1
                    passenger_set[i].velocity = get_velocity(passenger_set[i])

                    if is_at_block(passenger_set[i]):
                        # passenger_set[i].velocity =0.8
                        passenger_set[i].cury = 7 * passenger_set[i].target_block - 3
                        passenger_set[i].aisle_state = passenger_set[i].target_block

                else:
                    # passenger_set[i].velocity = get_blockk_velocity(passenger_set[i])
                    passenger_set[i].curx = passenger_set[i].curx + passenger_set[i].velocity * SIMULATION_TAU
                    if is_at_target(passenger_set[i]):
                        put_luggage(passenger_set[i])
            elif passenger_set[i].state == 1:
                # 等待哦
                if passenger_set[i].waiting_time_left > 0:
                    passenger_set[i].waiting_time_left = passenger_set[i].waiting_time_left - SIMULATION_TAU
                else:
                    passenger_set[i].state = 0
            elif passenger_set[i].state == 2:
                if passenger_set[i].luggage_time_left > 0:
                    passenger_set[i].luggage_time_left = passenger_set[i].luggage_time_left - SIMULATION_TAU
                else:
                    passenger_set[i].state = 3
            elif passenger_set[i].state == 3:
                block_position_set[passenger_set[i].target_block][get_block_cell(passenger_set[i])] = INFINITY
                finished.append(i)
        else:
            continue

print(time_step)
