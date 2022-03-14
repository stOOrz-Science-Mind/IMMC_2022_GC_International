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

csv_titles = [
    f'H:/stOOrz-Mathematical-Modelling-Group/IMMC_2022_International/Programming/simulation_of_plane_boarding/ours/different occasions/discompliance_output_csv_sigmoid_random/log{i}.csv'
    for i in range(10001)]


class passenger:
    def __init__(self, target_x=0, target_y=0, curx=0.00, cury=0.00, curcell=0, sequence=0, state=0, velocity=0,
                 density=0, luggage_time_left=0, waiting_time_left=0, unruly=1):
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
        self.unruly = unruly

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

unruly_index = [1.00004794, 1.00005151, 1.00006219, 1.00007123, 1.00007691, 1.00008462, 1.00009302,
                1.0000945, 1.00011179, 1.00011806, 1.00012623, 1.00015351, 1.00015739, 1.00023703, 1.00027413,
                1.00030675,
                1.0003632, 1.00037066, 1.00037757, 1.00038506, 1.00040367, 1.00044479, 1.00055885, 1.00059066,
                1.00061933,
                1.00076823, 1.00081775, 1.00085285, 1.00092161, 1.0009542, 1.00110578, 1.00116423, 1.00116927,
                1.00139169,
                1.00177131, 1.00184159, 1.00218485, 1.00224193, 1.00310921, 1.0032787, 1.00365205, 1.00416568,
                1.0045446,
                1.00460272, 1.00473473, 1.00477744, 1.00493622, 1.00512668, 1.00610499, 1.00715462, 1.00880232,
                1.01050179,
                1.01252208, 1.01461181, 1.01615364, 1.01824582, 1.01939855, 1.01951697, 1.01955589, 1.02846353,
                1.02978391,
                1.03101767, 1.03204033, 1.03591781, 1.03763251, 1.0381624, 1.05066995, 1.05675721, 1.05773988,
                1.05780358,
                1.06112839, 1.06398319, 1.06775096, 1.07438267, 1.0835929, 1.0842561, 1.09010232, 1.12258639,
                1.12846083,
                1.12866299, 1.14193409, 1.14932998, 1.16391513, 1.24278764, 1.24287547, 1.26377703, 1.27954028,
                1.30326948,
                1.31915523, 1.33046515, 1.38989511, 1.46213855, 1.51441009, 1.54405657, 1.54503282, 1.55355316,
                1.63437288,
                1.64809566, 1.66859984, 1.68116873, 1.73672815, 1.75425637, 1.75480188, 1.75864602, 1.76492943,
                1.7663399,
                1.79432684, 1.80397935, 1.8403837, 1.84982551, 1.85437483, 1.86459761, 1.86928425, 1.87452688,
                1.87479445,
                1.88192629, 1.89150076, 1.89230189, 1.89749604, 1.90713675, 1.90939374, 1.93058941, 1.93094293,
                1.93290565,
                1.94136311, 1.95505461, 1.95668491, 1.95929603, 1.96195086, 1.96406154, 1.96723282, 1.96947214,
                1.97216762,
                1.97856115, 1.97960577, 1.98127273, 1.98176395, 1.98318694, 1.98432316, 1.98552209, 1.9855228,
                1.98636245,
                1.98723872, 1.98908351, 1.9891858, 1.99069405, 1.9918292, 1.99304043, 1.99388833, 1.99436733,
                1.99464183,
                1.9951605, 1.99552967, 1.99583207, 1.99584267, 1.99664789, 1.99741966, 1.99753204, 1.99777147,
                1.9980502,
                1.99834654, 1.99839075, 1.99854389, 1.99861404, 1.99875408, 1.99900158, 1.99908537, 1.9992043,
                1.99924359,
                1.99927674, 1.99938589, 1.99940183, 1.99943062, 1.99949313, 1.99954103, 1.99964742, 1.99967086,
                1.99969531,
                1.9997028, 1.999749, 1.99981787, 1.99983342, 1.99984747, 1.99985804, 1.99989277, 1.99990168, 1.99993685,
                1.99993931, 1.99995114]

TIME_TO_PUT_LUGGAGE = 5  # s
targx = [8, 4, 27, 10, 9, 20, 23, 7, 4, 19, 24, 27, 32, 12, 10, 11, 27, 4, 11, 13, 21, 19, 29, 12, 20, 31, 10, 28, 1,
         18, 4, 14, 25, 10, 30, 23, 23, 10, 2, 24, 16, 14, 13, 32, 12, 25, 30, 32, 17, 20, 31, 9, 13, 26, 14, 15, 25,
         12, 9, 21, 3, 14, 20, 6, 12, 5, 9, 1, 17, 5, 22, 15, 5, 5, 1, 31, 16, 12, 22, 21, 3, 16, 29, 20, 30, 7, 30, 29,
         10, 7, 31, 8, 30, 6, 28, 15, 32, 14, 4, 26, 13, 28, 26, 23, 27, 6, 7, 30, 2, 17, 31, 2, 19, 15, 7, 14, 24, 23,
         27, 18, 21, 7, 16, 3, 28, 23, 26, 16, 26, 21, 3, 22, 9, 28, 25, 8, 19, 24, 8, 13, 11, 11, 31, 5, 26, 6, 18, 16,
         20, 32, 6, 24, 8, 2, 19, 8, 29, 11, 5, 18, 25, 29, 17, 21, 13, 17, 22, 17, 22, 24, 9, 3, 22, 4, 19, 25, 27, 2,
         28, 6, 32, 15, 29, 2, 18, 15, 11, 3, 18]
targy = [-1, 2, -2, 2, -1, 1, -1, -1, 3, 1, -2, -1, -2, 2, 1, -1, 1, -3, 3, 3, 1, -3, -3, 1, 3, -1, -2, -2, -2, -2, -1,
         -2, -1, -3, 1, 2, -2, -1, -3, 1, -3, 2, -3, 1, -3, 1, -3, -1, -3, -2, 3, 1, -2, -3, 1, 1, 3, -2, -2, -3, 1, 3,
         2, 3, 3, -2, -3, -3, 3, -1, 3, -1, 2, 1, -1, -2, 2, -1, -3, -1, 3, 3, -1, -1, 3, -2, 2, 3, 3, -3, 2, -2, -1,
         -2, -3, 2, 2, -1, 1, 2, 1, -1, 3, -3, 3, 2, 2, -2, 1, 2, -3, 2, 2, -2, 1, -3, 2, 3, -3, -1, -2, 3, -1, -3, 1,
         1, -2, -2, -1, 2, -1, -1, 3, 3, 2, -3, 3, -1, 3, 2, -2, 1, 1, 3, 1, 1, 2, 1, -3, -3, -1, -3, 2, -1, -2, 1, -2,
         2, -3, -3, -3, 1, -1, 3, -1, -2, 1, 1, 2, 3, 2, 2, -2, -2, -1, -2, 2, -2, 2, -3, 3, 3, 2, 3, 3, -3, -3, -2, 1]

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
    passenger_set[i].unruly = unruly_index[i]


####################################

def put_luggage(pasng):
    # f.write('$$$$$$$$$$$$$$$$$$$$$$$$')
    pasng.state = 2
    pasng.luggage_time_left = max(pasng.unruly * STANDARD_LUGGAGE_TIME, seating_time(pasng))
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
