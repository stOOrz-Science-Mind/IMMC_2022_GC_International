import matplotlib.pyplot as plt
import numpy as np

INTERVAL = 0.01


def get_random(n):  # between -1 and 1
    d = np.random.random(n + max(3, int(0.01 * n)))
    return d[np.where(d > 0)][:n] * 2 - 1


def withbounds_get_random(left, right, n):
    ans = (get_random(n) + 1) * (right - left) / 2 + left
    return ans


def plot_random_unsorted(left, right, n):
    datax = range(0, n)
    datay = withbounds_get_random(left, right, n)
    plt.plot(datax, datay)
    plt.legend(['non-compliace index unsorted'])
    plt.show()


def plot_random_sorted(left, right, n):
    datax = range(0, n)
    datay = withbounds_get_random(left, right, n)
    sorted_datay = np.sort(datay)
    plt.plot(datax, sorted_datay)
    plt.legend(['non-compliace index sorted'])
    plt.show()


def sigmoid_rudim(x):
    ans = -1 / (1 + np.exp(x))
    return ans


def sigmoid_function_translated(x, left=-10, right=10, down=-1, up=1, stretch_to=20):
    x_mid = (left + right) / 2
    y_mid = (down + up) / 2
    ans = (sigmoid_rudim((x - x_mid) * stretch_to / (right - left)) + y_mid) * 2 / (up - down)
    return ans


def plot_sigmoid(left=-10, right=10, down=-1, up=1, stretch_to=20):
    datax = np.arange(left, right, INTERVAL)
    datay = sigmoid_function_translated(datax, left, right, down, up, stretch_to)
    plt.plot(datax, datay)
    plt.show()


# plot_random_sorted(1, 2, 189)
# plot_sigmoid(left=-10, right=10, down=-1, up=1, stretch_to=20)
def plot_random_sigmoid(n, left, right, down, up, stretch_to=20):
    datax = range(0, n)
    rd = withbounds_get_random(left, right, n)
    datay = sigmoid_function_translated(rd, left, right, down, up)
    plt.plot(datax, datay)
    plt.show()


def plot_random_sorted_sigmoid(n, left, right, down, up, stretch_to=20):
    datax = range(0, n)
    rd = withbounds_get_random(left, right, n)
    datay = np.sort(sigmoid_function_translated(rd, left, right, down, up))
    plt.figure(figsize=(10, 10), dpi=800)
    plt.plot(datax, datay)
    plt.legend(['non-compliance index following a sigmoid pattern'], loc=2)
    plt.show()
    return datay


a = plot_random_sorted_sigmoid(189, -10, 10, 1, 3)
print(a)


