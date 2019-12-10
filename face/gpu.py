from numba import jit
import numpy as np

SIZE = 2000
x = np.random.random((SIZE, SIZE))

"""
给定n*n矩阵，对矩阵每个元素计算tanh值，然后求和。
因为要循环矩阵中的每个元素，计算复杂度为 n*n。
"""


@jit
def jit_tan_sum(a):  # 函数在被调用时编译成机器语言
    tan_sum = 0
    for i in range(SIZE):  # Numba 支持循环
        for j in range(SIZE):
            tan_sum += np.tanh(a[i, j])  # Numba 支持绝大多数NumPy函数
    return tan_sum


print(jit_tan_sum(x))
