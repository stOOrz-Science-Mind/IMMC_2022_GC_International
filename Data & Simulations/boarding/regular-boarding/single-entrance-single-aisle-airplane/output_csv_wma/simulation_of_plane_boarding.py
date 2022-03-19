import math
import sys
import csv
import os
import shutil

sys.setrecursionlimit(100)
f = open('log.txt', 'w')

csv_index_row = ['time_step',
                 'passenger_sequence',
                 'target_x',
                 'target_y',
                 'current_x',
                 'current_y',
                 'current_cell',
                 'state']

csv_titles = [f'C:/Users/Allan/Desktop/simulation_of_plane_boarding/output_csv_window_middle_aisle/log{i}.csv' for i in range(10001)]


class passenger:
    def __init__(self, target_x=0, target_y=0, curx=0.00, cury=0.00, curcell=0, sequence=0, state=0, velocity=0,
                 density=0, luggage_time_left=0, waiting_time_left=0):
        self.target_x = target_x  # 所在座位的行数，从前到后编号为 1,2,……
        self.target_y = target_y  # 所在座位的列数
        self.curx = curx
        self.cury = cury
        self.curcell = curcell  # 当前所在过道单元格
        self.sequence = sequence  # 排队的顺序
        self.state = state  # 0=在走路, 1=停止但没到, 2=停止且到了, 3=坐好了
        self.velocity = velocity
        self.density = density
        self.luggage_time_left = luggage_time_left  # 放行李还剩多少时间
        self.waiting_time_left = waiting_time_left  # 还要等多久

    def show(self):
        f.write(
            f'()()()()\n'
            f'target_x: {self.target_x}\n'
            f'target_y: {self.target_y}\n'
            f'curx: {self.curx}\n'
            f'cury: {self.cury}\n'
            f'curcell: {self.curcell}\n'
            f'sequence: {self.sequence}\n'
            f'state: {self.state}\n'
            f'velocity: {self.velocity}\n'
            f'density: {self.density}\n'
            f'()()()()()()()()')


VISIBILITY_RANGE = 4
PASSENGER_NUM = 189
TOTAL_AISLE_NUM = 500
AISLE_WITHIN_PLANE = 33  # 编号 0~ASILE_WITHIN_PLANE-1 都是在飞机内部的过道。所有过道从里到外编号。对于在飞机内部的过道，假设它的编号是i，那么它对应的行数是 ASILE_WITHIN_PLANE-1-i
INFINITY = 99999
NATURAL_VELOCITY = 0.8  # m/s
SEAT_WIDTH = 0.8  # m
SIMULATION_TAU = 1 / 3  # s
STANDARD_SEATING_TIME = 1  # s ,乘客横向移动一格需要的时间
STANDARD_LUGGAGE_TIME = 5  # s
UNRULY = 1  # 不守规则指数，越大越不守规则

TIME_TO_PUT_LUGGAGE = 5  # s
targx = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
         31, 32, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
         29, 30, 31, 32, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
         27, 28, 29, 30, 31, 32, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29, 30, 31, 32, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
         25, 26, 27, 28, 29, 30, 31, 32, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
         24, 25, 26, 27, 28, 29, 30, 31, 32]
targy = [-3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
         -3, -3, -3, -3, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2,
         -2, -2, -2, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
         2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

passenger_set = [0 for i in range(PASSENGER_NUM)]  # 乘客数组
position_set = [0 for i in range(
    TOTAL_AISLE_NUM)]  # the elements inside reperesent the boarding sequence of the passenger within this cell. INFINITY for nobody, 从里到外排。（飞机内最后一排对应0）
target_seatx_set = [0 for i in range(PASSENGER_NUM)]
target_seaty_set = [0 for i in range(PASSENGER_NUM)]


def is_anyone_in_the_cell(num):
    if position_set[num] == INFINITY:
        return False
    else:
        return True


def get_visibility(pasng):  # 返回拥堵指数 E.g. 前四格里有两个人，返回 0.5
    cnt = 0  # 前 VISIBILITY_RANGE 里面有多少乘客
    for i in range(pasng.curcell - 4, pasng.curcell):
        if is_anyone_in_the_cell(i):
            cnt = cnt + 1
    return (cnt / VISIBILITY_RANGE)


def get_vis(pasng):
    ans = []
    for i in range(pasng.curcell - 4, pasng.curcell):
        if is_anyone_in_the_cell(i):
            ans.append(position_set[i])
    return ans


def get_velocity(pasng):
    return NATURAL_VELOCITY * (1 - get_visibility(pasng))


def is_everyone_seated():  # 判断登机过程是否已经结束
    for i in range(PASSENGER_NUM):
        if passenger_set[i].state != 3:
            return False
    return True


def get_current_cell(pasng):  # output the cell of a passenger
    ans = math.floor(AISLE_WITHIN_PLANE - 0.5 - pasng.curx)
    return ans


def seating_time(pasng):
    ans = 0
    for i in range(pasng.sequence):
        if targx[i] == pasng.target_x and targy[i] * pasng.target_y > 0 and abs(targy[i]) < abs(pasng.target_y):
            ans = max(ans, targy[i])
        else:
            ans = 0
    return ans * STANDARD_SEATING_TIME


def get_the_cells_right_behind(pasng):
    ans = []
    the_cell = pasng.curcell
    for i in range(the_cell + 1, the_cell + 500):
        if i >= 490:
            continue

        else:
            if is_anyone_in_the_cell(i):
                ans.append(position_set[i])
    return ans


def is_at_target_seat(pasng):
    if pasng.curcell == AISLE_WITHIN_PLANE - 1 - pasng.target_x:
        return True
    else:
        return False


###################### initialize

for i in range(TOTAL_AISLE_NUM):  # 初始化过道单元格对应的乘客
    if i < AISLE_WITHIN_PLANE:  # 对于那些在飞机中的过道单元格，它们一开始没有被占用
        position_set[i] = INFINITY  # 没有人
    elif i >= AISLE_WITHIN_PLANE and i < AISLE_WITHIN_PLANE + PASSENGER_NUM:  # 一开始从飞机外的第一格开始排队
        position_set[i] = i - AISLE_WITHIN_PLANE  # 例如在舱外第一格是序号为0的乘客
    else:
        position_set[i] = INFINITY  # 只是预留一点空间

#################################### window-middle-aisle

for i in range(PASSENGER_NUM):
    passenger_set[i] = passenger()
    passenger_set[i].target_x = targx[i]
    passenger_set[i].target_y = targy[i]
    passenger_set[i].curx = -1 - i
    passenger_set[i].cury = 0.00
    passenger_set[i].curcell = get_current_cell(passenger_set[i])
    passenger_set[i].sequence = i
    passenger_set[i].state = 0
    passenger_set[i].velocity = get_velocity(passenger_set[i])
    passenger_set[i].density = get_visibility(passenger_set[i])
    passenger_set[i].luggage_time_left = 0
    passenger_set[i].waiting_time_left = 0


####################################

def put_luggage(pasng):
    # f.write('$$$$$$$$$$$$$$$$$$$$$$$$')
    pasng.state = 2
    pasng.luggage_time_left = max(UNRULY * STANDARD_LUGGAGE_TIME, seating_time(pasng))
    # f.write(str(get_the_cells_right_behind(pasng)))
    for j in get_the_cells_right_behind(pasng):
        if not is_at_target_seat(passenger_set[j]):
            passenger_set[j].state = 1
            passenger_set[j].waiting_time_left = pasng.luggage_time_left
        else:
            passenger_set[j].state = 2
            # passenger_set[j].curx = passenger_set[j].curx + 0.2
            # f.write("##########")
            # put_luggage(passenger_set[j])


def update_position_set():
    for i in range(TOTAL_AISLE_NUM):
        position_set[i] = INFINITY
    for i in range(PASSENGER_NUM):
        passenger_set[i].curcell = get_current_cell(passenger_set[i])
        position_set[passenger_set[i].curcell] = passenger_set[i].sequence
        if position_set[i] in already_done_no:
            position_set[i] = INFINITY


already_done_no = []  # 已经搞定的乘客的编号
time_step = 0
# while not is_everyone_seated():
while len(already_done_no) != 189:

    outputFile = open(csv_titles[time_step], 'w', newline='')
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow(csv_index_row)
    # outputWriter.writerow([1,2,3])

    time_step = time_step + 1  # 更新时间

    if time_step % 50 == 0:
        # f.write("----------------round " + str(time_step))
        print(already_done_no)
        # if time_step ==700:
    for i in range(PASSENGER_NUM):

        update_position_set()
        if i not in already_done_no:  # 如果 i 还没坐下

            if passenger_set[i].state == 0:
                passenger_set[i].curx = passenger_set[i].curx + SIMULATION_TAU * passenger_set[i].velocity
                passenger_set[i].curx = passenger_set[i].curx + 0.1
                passenger_set[i].velocity = get_velocity(passenger_set[i])
                passenger_set[i].density = get_visibility(passenger_set[i])
                passenger_set[i].curcell = get_current_cell(passenger_set[i])

                current_cell = passenger_set[i].curcell
                if is_at_target_seat(passenger_set[i]):  # 如果已经抵达放行李的位置，则进入放行李和让座模式
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
                position_set[passenger_set[i].curcell] = INFINITY
                already_done_no.append(passenger_set[i].sequence)
                passenger_set[i].curcell = 499
        else:
            continue
        outputWriter.writerow([time_step,
                             passenger_set[i].sequence,
                             passenger_set[i].target_x,
                             passenger_set[i].target_y,
                             passenger_set[i].curx,
                             passenger_set[i].cury,
                             passenger_set[i].curcell,
                             passenger_set[i].state])
        # outputWriter.writerow([f'test{i}'])
    outputFile.close()

f.write('FINAL TIME: ' + str(time_step))

f.close()
