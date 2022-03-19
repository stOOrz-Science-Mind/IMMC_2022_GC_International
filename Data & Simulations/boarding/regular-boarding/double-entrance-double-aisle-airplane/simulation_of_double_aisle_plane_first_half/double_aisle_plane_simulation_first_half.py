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
        self.aisle_state = aisle_state  # 0=主过道，1=块过道1，2=块过道2
        self.target_block = target_block  # 1，2

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


csv_index_row = ['time_step',
                 'passenger_sequence',
                 'target_x',
                 'target_y',
                 'current_x',
                 'current_y',
                 'current_cell',
                 'state']

csv_titles = [
    f'H:/stOOrz-Mathematical-Modelling-Group/IMMC_2022_International/Programming/simulation_of_double_aisle_plane_first_half/log{i}.csv'
    for i in range(10001)]
# class cell:
#     def __init__(self,state = 0,index = 0):
#         self.state = 0 # 0代表主
VISIBILITY_RANGE = 4
PASSENGER_NUM = 127
TOTAL_AISLE_NUM = 1000
INFINITY = 99999
NATURAL_VELOCITY = 0.8  # m/s
SEAT_WIDTH = 0.8  # m
SIMULATION_TAU = 1 / 3  # s
STANDARD_SEATING_TIME = 1  # s ,乘客横向移动一格需要的时间
STANDARD_LUGGAGE_TIME = 5  # s

BLOCK_AISLE_LENGTH = 20  # 同时考虑过道上的那个格
MAIN_AISLE_LENGTH = 1000  # 主过道预留足够空间


lower = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3),
         (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (5, 0), (5, 1), (5, 2),
         (5, 3), (5, 4), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (8, 0), (8, 1),
         (8, 2), (8, 3), (8, 4), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (10, 0), (10, 1), (10, 2), (10, 3), (10, 4),
         (11, 0), (11, 1), (11, 2), (11, 3), (11, 4), (12, 0), (12, 1), (12, 2), (12, 3), (12, 4), (13, 0), (13, 1),
         (13, 2), (13, 3), (13, 4), (14, 0), (14, 1), (14, 2), (14, 3), (14, 4), (15, 0), (15, 1), (15, 2), (15, 3),
         (15, 4), (16, 0), (16, 1), (16, 2), (16, 3), (16, 4), (17, 0), (17, 1), (17, 2), (17, 3), (17, 4), (18, 0),
         (18, 1), (18, 2), (18, 3), (18, 4), (19, 0), (19, 1), (19, 2), (19, 3), (19, 4), (1, 5), (3, 5), (5, 5),
         (7, 5), (9, 5), (11, 5), (13, 5), (15, 5), (17, 5), (19, 5)]

upper = [(0, 6), (0, 7), (0, 8), (0, 9), (1, 6), (1, 7), (1, 8), (1, 9), (2, 6), (2, 7), (2, 8), (2, 9), (3, 6), (3, 7),
         (3, 8), (3, 9), (4, 6), (4, 7), (4, 8), (4, 9), (5, 6), (5, 7), (5, 8), (5, 9), (6, 6), (6, 7), (6, 8), (6, 9),
         (7, 6), (7, 7), (7, 8), (7, 9), (8, 6), (8, 7), (8, 8), (8, 9), (9, 6), (9, 7), (9, 8), (9, 9), (10, 6),
         (10, 7), (10, 8), (10, 9), (11, 6), (11, 7), (11, 8), (11, 9), (12, 6), (12, 7), (12, 8), (12, 9), (13, 6),
         (13, 7), (13, 8), (13, 9), (14, 6), (14, 7), (14, 8), (14, 9), (15, 6), (15, 7), (15, 8), (15, 9), (16, 6),
         (16, 7), (16, 8), (16, 9), (17, 6), (17, 7), (17, 8), (17, 9), (18, 6), (18, 7), (18, 8), (18, 9), (19, 6),
         (19, 7), (19, 8), (19, 9), (2, 5), (4, 5), (6, 5), (8, 5), (10, 5), (12, 5), (14, 5), (16, 5), (18, 5)]


def get_block(pasng):  # 懒得写太多条件了，请确保输入没问题就行
    if (pasng.target_x, pasng.target_y) in upper:
        return 2
    elif (pasng.target_x, pasng.target_y) in lower:
        return 1


passenger_set = [0 for i in range(PASSENGER_NUM)]

targx = [19, 19, 17, 17, 15, 15, 13, 13, 11, 11, 9, 9, 7, 7, 5, 5, 3, 3, 1, 1, 18, 16, 12, 19, 19, 17, 17, 15, 15, 13,
         13,
         11, 11, 9, 9, 7, 7, 5, 5, 3, 3, 1, 1, 19, 10, 17, 8, 13, 6, 11, 4, 9, 2, 7, 18, 5, 18, 3, 16, 1, 16, 18, 14,
         18,
         14, 16, 12, 16, 12, 14, 10, 14, 10, 12, 8, 12, 8, 10, 6, 10, 6, 8, 4, 8, 4, 6, 2, 6, 2, 4, 19, 4, 18, 2, 17, 2,
         16, 19, 13, 18, 12, 17, 11, 16, 10, 13, 9, 12, 8, 11, 7, 10, 6, 9, 5, 8, 4, 7, 3, 6, 2, 5, 1, 4, 3, 2, 1]
targy = [9, 8, 9, 8, 9, 8, 9, 8, 9, 8, 9, 8, 9, 8, 9, 8, 9, 8, 9, 8, 5, 5, 5, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2,
         1,
         2, 1, 2, 1, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 9, 5, 8, 5, 9, 5, 8, 1, 9, 2, 8, 1, 9, 2, 8, 1, 9, 2, 8, 1, 9,
         2,
         8, 1, 9, 2, 8, 1, 9, 2, 8, 1, 9, 2, 8, 1, 6, 2, 6, 1, 6, 2, 6, 4, 6, 4, 6, 4, 6, 4, 6, 4, 6, 4, 6, 4, 6, 4, 6,
         4,
         6, 4, 6, 4, 6, 4, 6, 4, 6, 4, 4, 4, 4]

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
    elif pasng.cury >= 2.5 and pasng.cury <= 3.5:
        return 1
    elif pasng.cury >= 6.5 and pasng.cury <= 7.5:
        return 2


def get_main_cell(pasng):
    ans = int(7 - pasng.cury + 0.5)
    return ans


def get_block_cell(pasng):
    ans = int(pasng.curx + 0.5)
    return ans


def update_position_set():
    for i in range(3):
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
            if i >= 18:
                continue
            else:
                if is_anyone_in_block_cell(bl, i):
                    cnt = cnt + 1
    return (cnt / VISIBILITY_RANGE)


def get_velocity(pasng):
    return NATURAL_VELOCITY * (1 - get_visibility(pasng))


def is_at_block(pasng):
    if pasng.aisle_state == 0 and pasng.cury >= 4 * pasng.target_block - 1.5 and pasng.cury <= 4 * pasng.target_block - 0.5:
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
        for i in range(4 * (bl - 1) + 1, 600):
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
    passenger_set[i].target_block = get_block(passenger_set[i])
    passenger_set[i].velocity = get_velocity(passenger_set[i])
    passenger_set[i].luggage_time_left = 0
    passenger_set[i].waiting_time_left = 0


def get_blockk_velocity(pasng):
    cnt = 0
    bl = pasng.target_block
    for i in range(get_block_cell(pasng) + 1, max(get_block_cell(pasng), BLOCK_AISLE_LENGTH - 1)):
        if is_anyone_in_block_cell(bl, i):
            cnt = cnt + 1
    return NATURAL_VELOCITY * (1 - (cnt / VISIBILITY_RANGE))


time_step = 0
while len(finished) != PASSENGER_NUM:
    outputFile = open(csv_titles[time_step], 'w', newline='')
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow(csv_index_row)

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
                        passenger_set[i].cury = 4 * passenger_set[i].target_block - 1
                        passenger_set[i].aisle_state = passenger_set[i].target_block

                else:
                    if passenger_set[i].velocity == 0:
                        passenger_set[i].curx = passenger_set[i].curx + 0.1
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
        outputWriter.writerow([time_step,
                               passenger_set[i].sequence,
                               passenger_set[i].target_x,
                               passenger_set[i].target_y,
                               passenger_set[i].curx,
                               passenger_set[i].cury,
                               '{L}',
                               passenger_set[i].state])
    outputFile.close()

print(time_step)
