import math
import sys
import csv
import os
import shutil

sys.setrecursionlimit(100)
f = open('log.txt', 'w')




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

unruly_index = [0.2119,0.3909,0.7207,0.1986,0.8392,0.4558,0.7286,0.5224,0.4074,0.0702,0.478,0.6974,0.4984,0.7177,0.448,0.029,0.1174,0.7244,0.2709,0.9791,0.2712,0.1278,0.6005,0.8853,0.8586,0.3694,0.1434,0.9149,0.3662,0.0017,0.6523,0.815,0.4757,0.9986,0.254,0.7825,0.2019,0.1983,0.1683,0.2722,0.711,0.4287,0.7864,0.1288,0.3313,0.3724,0.6514,0.5845,0.5242,0.2989,0.0578,0.9571,0.5394,0.2737,0.6842,0.5241,0.0331,0.7355,0.1428,0.3022,0.5218,0.2238,0.2056,0.9298,0.0359,0.8935,0.3534,0.4492,0.6965,0.6171,0.4716,0.5442,0.8353,0.1641,0.5113,0.6688,0.4239,0.5993,0.9797,0.4544,0.0261,0.0888,0.8656,0.7017,0.1913,0.4518,0.1435,0.1961,0.905,0.8325,0.1832,0.6959,0.6527,0.6427,0.3132,0.0125,0.5876,0.9165,0.3155,0.1277,0.9721,0.2005,0.0978,0.3313,0.7907,0.0644,0.1081,0.2172,0.8949,0.6903,0.5459,0.0125,0.3215,0.0952,0.1271,0.9032,0.8051,0.9595,0.1172,0.4746,0.2964,0.2467,0.7712,0.5661,0.0618,0.4447,0.235,0.6556,0.5556,0.335,0.5395,0.2696,0.4292,0.3961,0.4179,0.2342,0.4238,0.7913,0.4111,0.0907,0.2317,0.7261,0.4805,0.24,0.3918,0.0225,0.2076,0.9447,0.0503,0.2236,0.0377,0.7111,0.696,0.7151,0.792,0.6286,0.9739,0.6047,0.6954,0.9526,0.2012,0.4608,0.2503,0.6367,0.1131,0.4396,0.0963,0.9083,0.0351,0.1563,0.0801,0.8515,0.8433,0.7462,0.6543,0.6197,0.9486,0.1723,0.0214,0.6255,0.7953,0.7361,0.8015,0.8644,0.5985,0.1244,0.2334,0.0156,0.9819
]

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

f.write('FINAL TIME: ' + str(time_step))

f.close()
